from setuptools import setup

setup(name='maxquant',
      packages=['maxquant',
                'maxquant.cli',
                ],
      version='0.0.1',
      entry_points={
          'console_scripts': [
              'maxquant-batch = maxquant.cli.batch:main',
              'maxquant-mqpar = maxquant.cli.mqpar:main',
          ]
      }, install_requires=['PyYAML']
      )
