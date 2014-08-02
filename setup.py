from setuptools import setup, find_packages

from jheatmap import VERSION, AUTHORS, CONTACT_EMAIL

setup(
	name = "jheatmap",
	version = VERSION,
	packages = find_packages(),

	# metadata
	author = AUTHORS,
	author_email = CONTACT_EMAIL,
	description = "Interactive jHeatmap javascript component for viewing dataframes in ipython notebooks",
	license = "UPF Free Source Code",
	keywords = "ipython, notebook",
	url = "http://jheatmap.github.io/jheatmap/",
	long_description = __doc__,

	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: Other/Proprietary License",
		"Environment :: Console",
		"Intended Audience :: Science/Research",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Topic :: Scientific/Engineering",
		"Topic :: Scientific/Engineering :: Bio-Informatics"
	]
)
