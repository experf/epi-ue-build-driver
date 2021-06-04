from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="epi-ue-build-driver",
    version="0.1.0",
    author="Expanded Performance Inc",
    author_email="neil@expand.live",
    description="BService to drive Unreal Engine builds on VMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://futurepeftect.live",
    packages=find_namespace_packages(include=['epi.ue.build.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
    install_requires=[
        # Everybody!
        "ue4cli==0.0.52",
        "ue4-ci-helpers==0.0.11",

        # Proto-buf RPC runtime
        "grpcio>=1.38.0,<2",

        # Windows
        "pywin32>=301; platform_system == 'Windows'",
    ],
    entry_points = {
        'console_scripts': [
            'epi-ue-build-driver = epi.ue.build.driver:main',
        ],
    }
)
