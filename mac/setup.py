from setuptools import setup

APP = ['cw_mac.py']
APP_NAME = "JumpWizard"
DATA_FILES = ['jump.pbm', 'jump.db']
OPTIONS = {
 'iconfile':'icon.icns',
 'argv_emulation': True,
 #'packages': ['certifi'],
}

setup(
	name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)