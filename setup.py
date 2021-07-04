""" Upload Pip
- python setup.py bdist_wheel
- twine upload dist/qttp-0.3.6-py3-none-any.whl
wisebeggar / Luvfami****
"""

from setuptools import setup, find_packages

setup(
    name                = 'qttp',

    version             = '0.3.6',

    description         = 'Quant Trading Tools Packages',

    author              = 'Taehun Kim',

    author_email        = 'smarthun0106@gmail.com',

    url                 = 'https://github.com/smarthun0106/qttp',

    download_url        = 'https://github.com/smarthun0106/qttp/archive/master.zip',

    install_requires    =  ['numpy', 'pandas', 'ccxt'],

    packages            = find_packages(exclude = []),

    keywords            = ['pypi deploy'],

    python_requires     = '>=3',

    package_data        = {},

    zip_safe            = False,

    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
