from enum import IntEnum
import msgpack

class LogLevel(IntEnum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10

class Logger:
    def __init__(self, name, producer, topic="logging", level=LogLevel.WARNING):
        self.name = name
        self.producer = producer
        self.level = level
        self.topic = topic

    async def critical(self, message, data=None):
        await self.log(LogLevel.CRITICAL, message, data)

    async def error(self, message, data=None):
        await self.log(LogLevel.ERROR, message, data)

    async def warning(self, message, data=None):
        await self.log(LogLevel.WARNING, message, data)

    async def info(self, message, data=None):
        await self.log(LogLevel.INFO, message, data)

    async def debug(self, message, data=None):
        await self.log(LogLevel.DEBUG, message, data)

    async def log(self, level, message, data=None):
        if level < self.level:
            return
        packet = msgpack.packb([level, message, data], use_bin_type=True)
        await self.producer.send_and_wait(self.topic, packet)