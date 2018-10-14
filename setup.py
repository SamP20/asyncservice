from setuptools import setup, find_namespace_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="samp20-asyncservice",
    version="1.0.0",
    author="Sam Partridge",
    description="Simple class to start and stop an asyncio service",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/samp20/uk-sampartridge-service',
    python_requires='~=3.7',
    py_modules=['uk.sampartridge.sockets']
)