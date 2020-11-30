from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coolutils',
    version='1.0',
    packages=['coolutils'],
    url='https://github.com/bobdadada/coolutils',
    long_description=long_description,
    author='Xingyu Bao',
    author_email='baoxingyubob@outlook.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
