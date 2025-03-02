from setuptools import setup, find_packages
from src.utils.constants import APP_VERSION
setup(
    name='dataset-merger',
    version=f'{APP_VERSION}',
    author='dtungpka',
    author_email='duongdoantung2k3@gmail.com',
    description='A Qt5 application for merging datasets from multiple program folders.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dtungpka/visl-dataset-merger',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)