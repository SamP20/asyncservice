import asyncio
import signal


def run(*runnables):
    loop = asyncio.get_event_loop()
    try:
        for runnable in runnables:
            loop.run_until_complete(runnable.start())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            for runnable in reversed(runnables):
                task = None
                try:
                    task = loop.create_task(runnable.stop())
                    loop.run_until_complete(task)
                except Exception as ex:
                    ctx = {
                        "message": "unhandled exception shutting down runnable",
                        "exception": ex,
                    }
                    if task is not None:
                        ctx["future"] = task
                    loop.call_exception_handler(ctx)
            _cancel_all_tasks(loop)
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            loop.close()


def _cancel_all_tasks(loop):
    to_cancel = asyncio.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(asyncio.gather(*to_cancel, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )

