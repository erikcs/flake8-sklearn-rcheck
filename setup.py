from __future__ import with_statement
import setuptools

requires = [
    "flake8 > 3.0.0",
    "scikit-learn"
]

setuptools.setup(
    name='flake8-sklearn-rcheck',
    version='0.1',
    description="check if `random_state` argument is set, plugin for flake8",
    keywords='flake8 scikit-learn random_state',
    author='Erik C. Fredriksen',
    author_email='erik.fredriksen@phdstudent.hhs.se',
    url='https://github.com/nuffe/flake8-sklearn-rcheck',
    license='MIT',
    py_modules=['flake8-sklearn-rcheck'],
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'flake8.extension': [
            'S = flake8_sklearn_rcheck:RandomStateCheck',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
