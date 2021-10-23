import magic
import aiohttp
import asyncio

class FileChek:
    def __init__(self):
        self.magic = magic.Magic(mime=True)
        self.session = aiohttp.ClientSession()

    async def check_attachments(self, attachments: 'List[Attachment]'):
        for att in attachments:
            async with self.session.get(att.url) as resp:
                if resp.status == 200:
                    check_bytes = await resp.content.read(128)
            type = self.magic.from_buffer(check_bytes)
            print(type)
        pass