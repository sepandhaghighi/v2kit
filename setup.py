# -*- coding: utf-8 -*-
"""Setup module."""
from setuptools import setup


def read_description() -> str:
    """Read README.md and CHANGELOG.md."""
    try:
        with open("README.md") as r:
            description = "\n"
            description += r.read()
        with open("CHANGELOG.md") as c:
            description += "\n"
            description += c.read()
        return description
    except Exception:
        return '''V2Kit is a lightweight and extensible Python toolkit for working with V2Ray proxy configurations and subscriptions.
        It provides a clean API for common operations such as protocol detection, configuration validation, config relabeling,
        and subscription encoding/decoding. The project is designed with simplicity, predictability, and composability in mind,
        making it suitable for automation scripts, proxy pipelines, networking tools, and future extensions around V2Ray ecosystem utilities.'''


setup(
    name='v2kit',
    packages=['v2kit', 'v2kit.models'],
    version='0.4',
    description='V2Kit: A Lightweight Toolkit for V2Ray Config Manipulation',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='Sepand Haghighi',
    author_email='me@sepand.tech',
    url='https://github.com/sepandhaghighi/v2kit',
    download_url='https://github.com/sepandhaghighi/v2kit/tarball/v0.4',
    keywords='v2ray v2ray-config v2ray-tools vmess vless trojan shadowsocks proxy subscription network',
    project_urls={
        'Source': 'https://github.com/sepandhaghighi/v2kit'},
    install_requires=[],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
    ],
    license='MIT')
