from setuptools import setup, find_packages


def read_requirements():

    with open("requirements.txt") as f:

        requirements = [requirement.split("#")[0].strip() for requirement in f.read().split("\n") if requirement[0] != "#"]
        return requirements


setup(
    version="1.0.0",
    name="Pyrler",
    description="A Parler client library",
    long_description="",
    url="https://github.com/cogsec-collaborative/Pyrler",
    author="Cognitive Security Collaborative",
    author_email="info@cogsec-collab.org",
    packages=find_packages(),
    install_requires=read_requirements()
)