from setuptools import setup

microlib_name = 'samp20.amqpservice'

setup(
    name=microlib_name,
    version="0.1.0",
    author="Sam Partridge",
    description="Async AMQP client service component and logger",
    packages=[microlib_name],
    install_requires=[
        "msgpack>=0.6,<0.7",
        "aio_pika>=5,<6",
        "samp20.asynclogger"
    ],
)