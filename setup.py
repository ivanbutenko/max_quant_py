from setuptools import setup

setup(name='maxquant',
      packages=['maxquant',
                'maxquant.cli',
                ],
      version='0.0.8',
      entry_points={
          'console_scripts': [
              'maxquant-batch = maxquant.cli.maxquant_batch:main',
              'maxquant-mqpar = maxquant.cli.maxquant_mqpar:main',
          ]
      }, install_requires=['ujson']
      )
