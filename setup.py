from setuptools import setup

__version__ = "0.9.0"
__url__ = "https://github.com/carlskeide/is-healthy"

setup(
    name="is-healthy",
    version=__version__,
    description="Mini healthcheck CLI",
    author="Carl Skeide",
    author_email="carl@skeide.se",
    license="MIT",
    keywords=[
        "healthcheck",
    ],
    classifiers=[],
    py_modules=[
        "is_healthy"
    ],
    include_package_data=True,
    zip_safe=False,
    url=__url__,
    download_url="{}/archive/{}.tar.gz".format(__url__, __version__),
    install_requires=[
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "is-healthy = is_healthy:cli",
        ]
    }
)
