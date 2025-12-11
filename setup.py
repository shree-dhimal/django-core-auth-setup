from setuptools import setup, find_packages

setup(
    name="common-core",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.0",
        "djangorestframework",
        "pytz",
        "django-redis",
        "redis",
    ],
    description="Common reusable core for all Django modules",
    author="shree-dhimal",
    url="git@github.com:shree-dhimal/django-core-auth-setup.git",
)