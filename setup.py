from setuptools import setup

setup(name='maxquant',
      packages=['maxquant',
                'maxquant.cli',
                ],
      version='0.0.3',
      entry_points={
          'console_scripts': [
              'maxquant = maxquant.cli.maxquant:main',
          ]
      }, install_requires=['ujson']
      )
