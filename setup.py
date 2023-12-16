# PyHarmonyOptimizer/setup.py

from setuptools import setup, find_packages

setup(
    name='PyHarmonyOptimizer',
    version='1.0.0',
    author='Abdulkadir Özcan',
    author_email='ornek@email.com',
    description='Harmony algoritması tabanlı optimizasyon modülü',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AutoPyloter/PyHarmonyOptimizer',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
