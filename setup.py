from setuptools import setup

setup(
    name='CommonUtilities',
    version='0.2.1',
    author='Mohamed Abdel-Hafiz',
    author_email='mohamed.abdel-hafiz@cuanschutz.edu',
    description='A group of commonly used functions.',
    install_requires=[
        'requests>=2',
        'keyring>=24',
        'scikit-learn>=1',
        'scipy>=1',
        'pyyaml>=6'
    ],
    packages=['CommonUtilities'],
    license='MIT',
)
