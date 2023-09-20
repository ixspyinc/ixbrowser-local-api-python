from setuptools import setup, find_packages

setup(name='ixbrowser-local-api',
      version='1.0.2',
      description='A client of ixBrowser local api',
      author='IXSPY Team',
      author_email='tech@ixspy.com',
      url='https://github.com/ixspyinc/ixbrowser-local-api-python',
      license='MIT',
      keywords='',
      packages=find_packages(),
      install_requires=['requests >= 2'],
      classifiers=["Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11"]
      )
