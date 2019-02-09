from setuptools import setup

APP = ['cw_mac.py']
APP_NAME = "JumpWizard"
DATA_FILES = ['jump.pbm', 's_ct.pbm', 's_nj.pbm', 's_ny.pbm', 'jump.db']
OPTIONS = {
 'iconfile':'icon/icon.icns',
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