from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bxypyutils',
    version='1.2',
    packages=['bxypyutils'],
    install_requires=['six'],
    url='https://github.com/bobdadada/bxypyutils',
    long_description=long_description,
    author='Xingyu Bao',
    author_email='baoxingyubob@outlook.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
