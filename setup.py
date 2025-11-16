from setuptools import setup
import os

APP = ['okwin.py']

# Những file/thư mục cần mang theo trong app
DATA_FILES = [
    'app4.ico',
    'OKWIN11.png',
    ('img', [os.path.join('img', f) for f in os.listdir('img')]),
    ('OKWIN11', [os.path.join('OKWIN11', f) for f in os.listdir('OKWIN11')]),
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app4.ico',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
