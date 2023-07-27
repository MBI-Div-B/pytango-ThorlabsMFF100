from setuptools import setup, find_packages

setup(
    name="tangods_thorlabsmff100",
    version="0.0.1",
    description="Tango Device Server to control motorized flip mirrors from Thorlabs: MFF101/102",
    author="Daniel Schick",
    author_email="dschick@mbi-berlin.de",
    python_requires=">=3.6",
    entry_points={"console_scripts": ["ThorlabsMFF100 = tangods_thorlabsmff100:main"]},
    license="MIT",
    packages=["tangods_thorlabsmff100"],
    install_requires=[
        "pytango",
        "thorpy @ git+https://github.com/MBI-Div-B/thorpy.git"
    ],
    url="https://github.com/MBI-Div-b/pytango-ThorlabsMFF100",
    keywords=[
        "tango device",
        "tango",
        "pytango",
    ],
)
