from setuptools import setup, find_packages

setup(name='ixbrowser_local_api',
      version='0.1.0',
      description='A client of ixBrowser local api',
      author='IXSPY Team',
      author_email='tech@ixspy.com',
      url='https://github.com/ixspyinc/ixbrowser-local-api-python',
      license='MIT',
      keywords='',
      project_urls={
          'Documentation': '',
          'Funding': '',
          'Source': '',
          'Tracker': '',
      },
      packages=find_packages(),
      install_requires=['requests >= 2'],
      python_requires='>=3'
      )
