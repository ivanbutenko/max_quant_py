from setuptools import setup

setup(name='maxquant',
      packages=['maxquant',
                'maxquant.cli',
                ],
      version='0.1.1',
      entry_points={
          'console_scripts': [
              'maxquant-batch = maxquant.cli.maxquant_batch:main',
              'maxquant-mqpar = maxquant.cli.maxquant_mqpar:main',
              # 'maxquant-mzxml = maxquant.cli.mzxml:main',
              # 'maxquant-mzml = maxquant.cli.mzml:main',
          ]
      }, install_requires=['ujson', 'simple-drmaa-scheduler>=0.0.6']
      )
