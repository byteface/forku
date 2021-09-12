from setuptools import setup, find_packages

with open("README.md", "r") as f:
        long_description=f.read()

version = '0.0.2'

setup(
  name='forku',
  version=version,
  author="@byteface",
  author_email="byteface@gmail.com",
  license="MIT",
  url='https://github.com/byteface/forku',
  download_url='https://github.com/byteface/forku/archive/' + version + ' .tar.gz',
  description='Forks a library you have patched...',
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords=['fork', 'patch'],
  python_requires='>=3.6',
  classifiers=[
      "Programming Language :: Python :: 3",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License",
      "Topic :: Software Development",
      "Topic :: Terminals",
      "Topic :: Utilities",
      'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  install_requires=[
  ],
  packages=find_packages(),
  include_package_data=True,
)
