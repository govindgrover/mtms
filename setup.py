import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name							=	"mtms"
	, version						=	"1.0.2"
	, author						=	"Govind Grover"
	, author_email					=	"ask@govindgrover.com"
	, description					=	"Metro Train Management System"
	, long_description				=	long_description
	, long_description_content_type	=	"text/markdown"
	, url							=	"https://github.com/govindgrover/mtms"
	, project_urls					=	{
	}
	, classifiers					=	[
		"Programming Language :: Python :: 3"
		, "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
		, "Operating System :: OS Independent"
		, "Natural Language :: English"
		, "Natural Language :: Hindi"
		, "Topic :: Education"
	]
	, package_dir					=	{
		""	:	"src"
	}
	, package_data					=	{
		""	:	["initials/database/*.sql", "initials/lang/*.json", "lang/*.json"]
	}
	, packages						=	setuptools.find_packages(where="src")
	, python_requires				=	">=3.6"
	, install_requires 				=	[
		'mysql.connector'
		, 'uuid'
		, 'pyqrcode'
	]
)
