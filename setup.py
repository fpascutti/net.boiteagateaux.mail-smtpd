import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="net.boiteagateaux.mail-smtpd",
    version="0.0.1",
    author="Franck Pascutti",
    description="Simple SMTP daemon used for mail.boiteagateaux.net accounts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/fpascutti/net.boiteagateaux.mail-smtpd/",
    project_urls={
        "Source": "https://github.com/fpascutti/net.boiteagateaux.mail-smtpd/",
        "Tracker": "https://github.com/fpascutti/net.boiteagateaux.mail-smtpd/issues",
    },
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "bag-smtpd=bag_smtpd:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: No Input/Output (Daemon)",
        "Topic :: Communications :: Email",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiosmtpd>=1.2",
        "atpublic>=1.0",
    ],
)
