import pypi
 
packpath = "pyqtree.py"
pypi.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="Pyqtree",
                   description="A pure Python QuadTree spatial index for GIS or rendering usage.",
                   url="http://github.com/karimbahgat/PyQuadTree",
                   keywords="GIS spatial index quad tree",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 4 - Beta",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop',
                                "Topic :: Scientific/Engineering :: GIS"],
                   )

pypi.generate_docs(packpath) #!! WRONG TYPE, INCLUDES VARS AND SOURCE???
#pypi.upload_test(packpath)
pypi.upload(packpath)

## UPDATE/REPLACE ON PYPI W NEW NAME......
