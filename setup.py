try: from setuptools import setup
except: from distutils.core import setup

setup(	long_description=open("README.rst").read(), 
	name="""PyQuadTree""",
	license="""MIT""",
	author="""Karim Bahgat""",
	author_email="""karim.bahgat.norway@gmail.com""",
	py_modules=['pyqtree'],
	url="""http://github.com/karimbahgat/PyQuadTree""",
	version="""0.22""",
	keywords="""GIS spatial index quad tree""",
	classifiers=['License :: OSI Approved', 'Programming Language :: Python', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Intended Audience :: End Users/Desktop', 'Topic :: Scientific/Engineering :: GIS'],
	description="""A pure Python QuadTree spatial index for GIS or rendering usage.""",
	)
