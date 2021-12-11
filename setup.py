from distutils.core import setup
import os
from ssh4plib import version

long_description = """a shell ssh manager tools for python"""

setup(
    name="ssh4p",
    version=version.VERSION,
    author="xzcoder",
    author_email="zhushuai_it@163.com",
    description=long_description,
    long_description=long_description,
    platforms=['linux', 'macos'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Clustering",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
    ],
    packages=['ssh4plib'],
    scripts=[os.path.join("bin", p) for p in ["zssh", "zscp", "zssh-manager"]],
    install_requires=["pexpect"]
)
