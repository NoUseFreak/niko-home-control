import setuptools

setuptools.setup(
    name='niko-home-control',
    description='SDK for Niko Home Control',
    license='MIT',
    url='https://github.com/NoUseFreak/niko-home-control',
    version='0.3.0',
    author='Dries De Peuter',
    author_email='dries@nousefreak.be',
    maintainer='Dries De Peuter',
    maintainer_email='dries@nousefreak.be',
    long_description='Niko Home Control Client Library',
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=['nclib', 'netaddr', 'netifaces'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
)
