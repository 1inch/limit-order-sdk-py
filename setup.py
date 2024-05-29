from setuptools import setup, find_packages

setup(
    name="limit-order-sdk",
    version="0.9.0",
    package_dir={"": "limit_order_sdk"},  # Tells setuptools that packages are under limit_order_sdk
    packages=find_packages(where="limit_order_sdk"),  # Automatically find all packages in slimit_order_sdk
    install_requires=["web3", "requests"],
    extras_require={"dev": ["pytest", "twine", "build"]},
    python_requires=">=3.11, <3.15",
    author="1inch, dodgervl",
    author_email="",
    description="1inch Limit Order Protocol v4 SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/1inch/limit-order-sdk-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
