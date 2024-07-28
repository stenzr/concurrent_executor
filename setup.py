from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="spawn_parallel_instances",
    version="1.0.2",
    description="A package to run multiple instance of the same script.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/stenzr/spawn_parallel_instances",
    author="Rohit Kumar",
    author_email="rkrohitkr01@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'spawn_parallel_instances=spawn_parallel_instances.__main__:main',
        ],
    },
    install_requires=install_requires,
    python_requires='>=3.6',
    extras_require={
        'test': ['unittest', 'coverage'],
    },
)
