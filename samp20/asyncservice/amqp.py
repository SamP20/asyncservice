import aio_pika
import logging
from .logger import AsyncHandler, DictFormatter
import gzip
import json
import msgpack


class AmqpService:
    def __init__(self, config):
        self.config = config

    async def start(self):
        self.connection = await aio_pika.connect_robust(**self.config)

    async def stop(self):
        await self.connection.close()

    def __getattr__(self, name):
        return getattr(self.connection, name)


class AmqpLogHandler(AsyncHandler):
    def __init__(
        self,
        service,
        client_name,
        encoder=None,
        exchange="logging",
        logger=logging.getLogger(),
        level=logging.NOTSET,
    ):
        super().__init__(logger, level)
        self.service = service
        self.exchange = exchange
        self.client_name = client_name
        if encoder is None:
            import msgpack

            self.encoder = lambda d: msgpack.packb(d, use_bin_type=True, default=str)
        else:
            self.encoder = encoder
        self.formatter = DictFormatter()

    async def start(self):
        channel = await self.service.channel()
        self.exchange = await channel.declare_exchange(
            name="amq.topic", type=aio_pika.ExchangeType.TOPIC, durable=True
        )
        await super().start()

    async def emit_async(self, record):
        document = self.format(record)
        data = self.encoder(document)
        routing_key = ".".join(["log", record.levelname, self.client_name, record.name])
        await self.exchange.publish(
            aio_pika.Message(body=data, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key=routing_key,
        )


def decode(message: aio_pika.Message):
    ctype = message.content_type
    cenc = message.content_encoding
    body = message.body
    if cenc == "gzip":
        body = gzip.decompress(body)
    if ctype == "application/json":
        return json.loads(body)
    if ctype == "application/msgpack" or ctype == "application/x-msgpack":
        return msgpack.loads(body, raw=False)
