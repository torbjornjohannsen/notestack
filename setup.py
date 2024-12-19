from setuptools import setup

setup(
    name="notestack",
    version="0.1",
    packages=["notestack"],
    entry_points={
        'console_scripts': [
            'notestack = notestack.main:run',  # Invoke main function in myscript.main
        ],
    },
)