from setuptools import find_packages, setup

setup(
    name='flask-ml-server',
    version='0.1.0',
    license='GPLv3',
    author='Petros Lamb',
    author_email='petroslamb@yahoo.gr',
    description='A simple web service for tensorflow models',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-dotenv',
        'Flask',
        'Flask-Restplus',
        'tensorflow',
        'gensim',
        'Flask-Testing',
        'coverage',
        'flake8'
    ],
    entry_points = {
        'console_scripts': [
            'my-server-manage = scripts.manage:cli'
        ]
    }
)