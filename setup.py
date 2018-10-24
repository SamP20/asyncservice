from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="samp20-asyncservice",
    version="1.1.0",
    author="Sam Partridge",
    description="Base to build microservices upon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SamP20/asyncservice",
    python_requires="~=3.7",
    packages=find_namespace_packages(),
    install_requires=["msgpack", "aio_pika"],
)
