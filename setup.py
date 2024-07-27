from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="concurrent_executor",
    version="1.0.0",
    description="A package to run multiple instance of the same script.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/stenzr/concurrent_executor",
    author="Rohit Kumar",
    author_email="rkrohitkr01@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'concurrent_executor=concurrent_scripts.__main__:main',
        ],
    },
    install_requires=install_requires,
    python_requires='>=3.6',
    extras_require={
        'test': ['unittest', 'coverage'],
    },
)
