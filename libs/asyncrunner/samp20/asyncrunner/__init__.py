import asyncio
import signal


async def runner(*runnables):
    loop = asyncio.get_running_loop()
    current_task = asyncio.current_task(loop)

    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(s, current_task.cancel)

    for runnable in runnables:
        await runnable.start()

    try:
        while True:
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        for runnable in reversed(runnables):
            try:
                await runnable.stop()
            except Exception as ex:
                ctx = {
                    "message": "unhandled exception shutting down runnable",
                    "exception": ex,
                }
                loop.call_exception_handler(ctx)

def run(*runnables):
    asyncio.run(runner(*runnables))