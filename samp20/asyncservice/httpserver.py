from .service import Service
from aiohttp import web
import asyncio
import shutil
import os

class HttpServer(Service):
    def __init__(self, config):
        self.path = config.get('path')
        self.user = config.get('user')
        self.group = config.get('group')
        self.permissions = config.get('permissions')
        self.host = config.get('host', 'localhost')
        self.port = int(config.get('port', 8080))

    async def start(self):
        loop = asyncio.get_running_loop()
        self.http_server = web.Server(self.handle_request)
        if self.path is None:
            self.socket_server = await loop.create_server(self.http_server, self.host, self.port)
        else:
            self.socket_server = await loop.create_unix_server(self.http_server, self.path)
            if self.user is not None or self.group is not None:
                shutil.chown(self.path, self.user, self.group)
            if self.permissions is not None:
                os.chmod(self.path, int(self.permissions, 8))

    async def stop(self):
        self.socket_server.close()
        await self.socket_server.wait_closed()
        await self.http_server.shutdown(30)

    async def handle_request(self, request):
        raise NotImplementedError()