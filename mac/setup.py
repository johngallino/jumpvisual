from setuptools import setup

APP = ['jazzsoft-mac.py']
APP_NAME = "JumpVisualDB"
DATA_FILES = ['dispatch.pbm', 'jump.db', 'photographers']
OPTIONS = {
 'iconfile':'icon/jvdb-round.icns',
 'argv_emulation': False,
 #'packages': ['certifi'],
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)