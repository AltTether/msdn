from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='msdn',
    version='0.0.1',
    description='An API for Mastodon',
    long_description=readme,
    author='NODA Shumpei',
    author_email='200351p@ugs.kochi-tech.ac.jp',
    install_requires=['requests'],
    url='https://github.com/AltTether/msdn',
    license=license,
    packages=find_packages(exclude=('tests'))
)
