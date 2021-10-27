import magic
import aiohttp
import logging
import concurrent.futures
from wand.image import Image
import asyncio
import settings
import discord
from wand.display import display
from multiprocessing import Process, Queue

logger = logging.getLogger('main')


class FileConvert:
    def __init__(self):
        self.magic = magic.Magic(mime=True)
        self.session = aiohttp.ClientSession()

    async def check_attachments(self, message):
        result = []
        for att in message.attachments:
            async with self.session.get(att.url) as resp:
                if resp.status == 200:
                    file_bytes = await resp.content.read(128)

            mime_file = self.magic.from_buffer(file_bytes)
            if "image" in mime_file:
                result.append(await att.read())
        return result

    def convert_image(self, byte_file: bytes):
        with Image(blob=byte_file) as img:
            if (img.width, img.height) != (256, 256):
                img.resize(256, 256)
                img.filename = "image_to_test"
                img.format = "png"
                return img.make_blob()
            else:
                img.filename = "image_to_test"
                img.format = "png"
                return img.make_blob()


file_convert = FileConvert()


async def check_image(session, pool, loop, bytes_file, event):
    image256 = await loop.run_in_executor(pool,
                                          convert_image,
                                          bytes_file)
    async with session.post(f"{settings.server_url}/check_file",
                            data={"file": image256}) as response:
        if event.is_set():
            return
        result = await response.json()
    if not result.get("file_hash"):
        return
    if result["unsafe"] > settings.coefficient_unsafe:
        logger.info(f"Remove image hash: {result['file_hash']}")
        event.set()


async def remove_message(event, lock, message):
    await event.wait()
    channel = message.channel
    try:

        await channel.send(
            f"{message.author.mention} your message can contain 18+ content.")
        await message.delete()
        lock.release()
    except discord.Forbidden as e:
        pass
    except discord.NotFound as e:
        pass
    except discord.HTTPException as e:
        pass


async def close_tasks(lock, tasks):
    await lock.acquire()
    async for task in tasks:
        task.cancel()


def convert_image(bytes_file):
    """some python Magic?"""
    return file_convert.convert_image(bytes_file)


async def check_attachments(message):
    bytes_list = await file_convert.check_attachments(message)
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    lock = asyncio.Lock()
    asyncio.create_task(remove_message(event, lock, message))

    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as pool:
        async with aiohttp.ClientSession(
                headers={"token": settings.server_token}) as session:
            tasks = [asyncio.create_task(
                check_image(session, pool, loop, bytes_file, event))
                for bytes_file in bytes_list]
            close__task_f = asyncio.create_task(close_tasks(lock, tasks))
            done, pending = await asyncio.wait(tasks)
            close__task_f.cancel()

# return result
