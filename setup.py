from distutils.core import setup

setup(
    # Application name:
    name="EmployeeTimeTracker",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="dil kuwor",
    author_email="dil.kuwor@gmail.com",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="",

    #
    # license="LICENSE.txt",
    description="Employee Project Time Tracker.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
        "flask_apispec",
        "flask_restful",
        "validate_email",
        "pymongo",
        "bson",
        "apispec"
    ],
)