import asyncio
import logging
import msgpack

class AsyncHandler(logging.Handler):
    _sentinel = None    

    async def start(self):
        self.queue = asyncio.Queue()
        self.loop = asyncio.get_running_loop()
        self.read_task = self.loop.create_task(self.read_queue())

    async def stop(self):
        self.queue.put_nowait(self._sentinel)
        await self.read_task

    def emit(self, record):
        self.loop.call_soon_threadsafe(self.queue.put_nowait, record)

    async def emit_async(self, record):
        raise NotImplementedError('emit_async must be implemented '
                                  'by AsyncHandler subclasses')

    async def read_queue(self):
        while True:
            record = await self.queue.get()
            if record is self._sentinel:
                break
            try:
                await self.emit_async(record)
            except:
                self.handleError(record)


class DictFormatter(logging.Formatter):
    DEFAULT_PROPERTIES = logging.LogRecord(
        '', '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        document = {
            'created': record.created,
            'level': record.levelname,
            'thread': record.thread,
            'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': record.name,
            'filename': record.pathname,
            'module': record.module,
            'method': record.funcName,
            'lineNumber': record.lineno
        }
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        return document


class AmqpHandler(AsyncHandler):
    def __init__(self, channel, exchange, client_name, level=logging.NOTSET):
        super().__init__(level)
        self.channel = channel
        self.exchange = exchange
        self.client_name = client_name

    async def emit_asymc(self, record):
        document = self.format(record)
        data = msgpack.packb(document, use_bin_type=True, default=str)
        routing_key = '.'.join([self.client_name, record.name, record.levelname])
        await self.channel.publish(data, exchange_name=self.exchange, routing_key=routing_key)