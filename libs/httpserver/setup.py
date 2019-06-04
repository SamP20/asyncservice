from setuptools import setup

microlib_name = 'samp20.httpserver'

setup(
    name=microlib_name,
    version="0.1.0",
    author="Sam Partridge",
    description="Base library for an http server component",
    packages=[microlib_name],
    install_requires=["aiohttp>=3.5,<4"],
)