from setuptools import setup, find_packages

setup(
    name="octane-installer",
    version="0.9.0",
    packages=find_packages(),
    include_package_data=True,
    description="Octane Installer",
    install_requires=[
        "pyinstaller",
    ],
    entry_points={
        "console_scripts": [
            "octane-installer=installer:main",
        ],
    },
)