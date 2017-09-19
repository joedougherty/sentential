try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
        name='sentential',
        version='0.0.7',
        description="A sentential logic interpreter/evaluator.",
        author_email='joseph.dougherty@gmail.com',
        packages=['sentential'],
        install_requires=['prettytable', 'pytest', 'coverage'],
        package_data={
            '': ['LICENSE', 'NOTICE', '*.rst'],
            },
        classifiers=(
           'Programming Language :: Python',
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3',
           'Programming Language :: Python :: 3.5',
           'Development Status :: 4 - Beta',
           'Environment :: Console',
           'Intended Audience :: End Users/Desktop',
           'Intended Audience :: Education',
           'Intended Audience :: Science/Research',
        ),
)
