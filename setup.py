from setuptools import setup


def readme():
    with open('README.rst') as infile:
        return infile.read()

setup(
  name='Coding Booth',
  version='0.0.1',
  long_description=readme(),
  packages=['codingbooth'],
  include_package_data=True,
  zip_safe=False,
  install_requires=['Flask>=0.8', 'pymongo>=2.3', 'pyzmq>=2.2.0.1']
)
