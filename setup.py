from setuptools import setup, find_packages

setup(
        packages=find_packages(),
        python_requires='>=3.11.0',
        install_requires=[
            'click',
            ],
        entry_points={
            'console_scripts': [
                'rsyncer = rsyncer.rsyncer:rsyncer',
                ]
            }
        )


