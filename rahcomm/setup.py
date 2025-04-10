from setuptools import setup, find_packages

setup(
    name="rahcomm",
    version="0.0.0",
    description="RAH Communication Tool for FPGA data communication on Vaaman.",
    author="Shail Parmar",
    author_email="shailparmar26@gmail.com.com",
    packages=find_packages(),
    install_requires=[
        "pyrah"
    ],
    entry_points={
        "console_scripts": [
            "rahcomm=rahcomm.main:main",
        ],
    },
)

