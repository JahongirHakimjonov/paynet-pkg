import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

keywords = "paynet, paynet-merchant, paynet-pkg, paynet-api, paynet-python-integration, paynet-integration, paynet-python, paynet-gateway, paynet-payment, paynet-payment-gateway, paynet-integration-python, paynet-api-client, paynet-django, paynet-rest-api" # noqa

setup(
    name='paynet-pkg',
    version='0.1',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages(),
    url='https://github.com/Muhammadali-Akbarov/paynet-pkg',
    keywords=keywords,
    install_requires=[
        'requests==2.*',
        "dataclasses==0.*;python_version<'3.7'",  # will only install on py3.6
        'djangorestframework==3.*'
      ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
