from setuptools import find_packages, setup

setup(
    name="row_cleaner",
    version="0.1.0",
    packages=find_packages(include=["postgresrowscleaner"]),
    description="A package to clean up unwanted rows from postgrestable",
    author = "Anish Karki",
    install_requires=["psycopg2","configparser"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)