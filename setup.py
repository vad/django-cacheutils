try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires = [
    'Django>=1.4',
]

long_description = open('README.rst').read()

setup(
    name='django-cacheutils',
    version="0.1",
    description='Django cache for Ponies',
    url='http://github.com/ahref/django-cacheutils',
    packages=['cacheutils'],
    zip_safe=True,
    license='BSD',
    classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
    long_description=long_description,
    install_requires=install_requires,
)
