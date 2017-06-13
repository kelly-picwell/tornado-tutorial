import os.path
import setuptools

from tornado_tutorial import version


def read_requirements(filename):
    requirements = []
    try:
        with open(os.path.join('requires', filename)) as req_file:
            for line in req_file:
                requirements.append(line.strip())
    except IOError:
        pass
    return requirements


requirements = read_requirements('installation.txt')
tests_require = read_requirements('testing.txt')

setuptools.setup(
    name='tornado_tutorial',
    version=version,
    author='Picwell',
    author_email='kelly@picwell.com',
    install_requires=requirements,
    namespace_packages=['tornado_tutorial'],
    packages=setuptools.find_packages(),
    entry_points={
        'distutils.commands': ['run=tornado_tutorial:main'],
    },
    test_suite='nose.collector',
    tests_require=tests_require,
    zip_safe=True,
)
