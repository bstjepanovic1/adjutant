import setuptools

setuptools.setup(
    name="adjutant",
    version="0.0.1",
    description="""
        Python tool for source code generation and processing.
    """,
    author="Boban Stjepanovic",
    author_email="bstjepanovic88@gmail.com",
    url="https://github.com/bstjepanovic1/adjutant",
    packages=['adjutant'],
	scripts=['bin/adjutant'],
    zip_safe=False,
)
