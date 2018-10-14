import logging
import asyncio
import signal

class Service:
    async def start(self):
        raise NotImplementedError()

    async def stop(self):
        raise NotImplementedError()

    async def run(self):
        loop = asyncio.get_running_loop()
        self._finished_future = loop.create_future()
        loop.add_signal_handler(signal.SIGINT, self.shutdown)
        loop.add_signal_handler(signal.SIGTERM, self.shutdown)
        await self.start()
        await self._finished_future
        await self.stop()

    def shutdown(self):
        if not self._finished_future.done():
            self._finished_future.set_result(None)