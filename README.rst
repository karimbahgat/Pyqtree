Pyqtree
=======

Pyqtree is a pure Python spatial index for GIS or rendering usage. It
stores and quickly retrieves items from a 2x2 rectangular grid area, and
grows in depth and detail as more items are added. The actual quad tree
implementation is adapted from `Matt Rasmussen's compbio
library <https://github.com/mdrasmus/compbio/blob/master/rasmus/quadtree.py>`__
and extended for geospatial use.

Platforms
---------

Python 2 and 3.

Dependencies
------------

Pyqtree is written in pure Python and has no dependencies.

Installing It
-------------

Installing Pyqtree can be done by opening your terminal or commandline
and typing:

::

    pip install pyqtree

Alternatively, you can simply download the "pyqtree.py" file and place
it anywhere Python can import it, such as the Python site-packages
folder.

Example Usage
-------------

Start your script by importing the quad tree.

::

    from pyqtree import Index

Setup the spatial index, giving it a bounding box area to keep track of.
The bounding box being in a four-tuple: (xmin, ymin, xmax, ymax).

::

    spindex = Index(bbox=(0, 0, 100, 100))

Populate the index with items that you want to be retrieved at a later
point, along with each item's geographic bbox.

::

    # this example assumes you have a list of items with bbox attribute
    for item in items:
        spindex.insert(item, item.bbox)

Then when you have a region of interest and you wish to retrieve items
from that region, just use the index's intersect method. This quickly
gives you a list of the stored items whose bboxes intersects your region
of interests.

::

    overlapbbox = (51, 51, 86, 86)
    matches = spindex.intersect(overlapbbox)

There are other things that can be done as well, but that's it for the
main usage!

More Information:
-----------------

-  `Home Page <http://github.com/karimbahgat/Pyqtree>`__
-  `API Documentation <http://pythonhosted.org/Pyqtree>`__

License:
--------

This code is free to share, use, reuse, and modify according to the MIT
license, see LICENSE.txt.

Credits:
--------

-  Karim Bahgat (2015)
-  Joschua Gandert (2016)

Changes
-------

0.25.0 (2016-06-22)
~~~~~~~~~~~~~~~~~~~

-  Misc user contributions and bug fixes

0.24.0 (2015-06-18)
~~~~~~~~~~~~~~~~~~~

-  Previous stable PyPI version.
