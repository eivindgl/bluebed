from setuptools import setup

setup(name='bluebed',
      version='0.1',
      description='A simple download interface to the deepblue API',
      url='http://github.com/eivindgl/bluebed',
      author='Eivind Gard Lund',
      author_email='gardlund@gmail.com',
      license='MIT',
      packages=['bluebed'],
      entry_points = {
        'console_scripts': ['bluebed=bluebed.dhs_example:main'],
      }
      )
