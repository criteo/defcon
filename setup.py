import os
from setuptools import find_packages, setup
from pip.req import parse_requirements

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = parse_requirements('requirements.txt', session='')
install_requires = [str(v.req) for v in install_requires]

test_require = parse_requirements('tests-requirements.txt', session='')
test_require = [str(v.req) for v in test_require]

setup(
    name='defcon',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    install_requires=install_requires,
    tests_require=test_require,
    description='defcon.',
    long_description=README,
    url='http://github.com/iksaif/defcon',
    author='Corentin Chary',
    author_email='corentin.chary@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
