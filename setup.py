try:
    from setuptools import setup, Extension
except ImportError:
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")

setup(
    name='datetime-distance',
    url='https://github.com/dedupeio/datetime-distance',
    version='0.1.2',
    description='Compare string distances between dates, timestamps, or datetime objects.',
    packages=['datetime_distance'],
    install_requires=['python-dateutil',
                      'future'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis']
)
