import magic
import aiohttp
import concurrent.futures
from wand.image import Image
import asyncio
import settings
from wand.display import display
from multiprocessing import Process, Queue


class FileChek:
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
                img.sample(256, 256)
                img.filename = "image_to_test"
                img.format = "png"
                return img.make_blob()
            else:
                img.filename = "image_to_test"
                img.format = "png"
                return img.make_blob()


file_check = FileChek()


def convert_images(bytes_list):
    result = []
    for byte in bytes_list:
        result.append(file_check.convert_image(byte))
    return result


async def check_image(session, bytes_file):
    async with session.post(f"http://{settings.server_url}/check_file",
                            data={"file": bytes_file}) as response:
        return await response.json()


async def check_attachments(message):
    bytes_list = await file_check.check_attachments(message)
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        image_list = await loop.run_in_executor(
            pool, convert_images, bytes_list)
    async with aiohttp.ClientSession(
            headers={"token": settings.server_token}) as session:
        tasks = [asyncio.ensure_future(check_image(session, bytes_file)) for
                 bytes_file in image_list]
        result = await asyncio.gather(*tasks)

    return result
