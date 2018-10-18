import asyncio
import signal

def interrupt_future():
    loop = asyncio.get_running_loop()
    finished_future = loop.create_future()

    def shutdown(self):
        if not finished_future.done():
            finished_future.set_result(None)

    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.add_signal_handler(signal.SIGTERM, shutdown)
    return finished_future

    