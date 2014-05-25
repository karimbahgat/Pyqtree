# Documentation for PyQuadTree

A pure Python QuadTree spatial index for GIS or rendering usage.

Karim Bahgat, 2014

Version: 0.2

License: MIT

Platforms: Python 2x and 3x

Based on Matt Rasmussen's original code:
https://github.com/mdrasmus/compbio/blob/master/rasmus/quadtree.py

## Installing It

Installing PyQuadTree is as easy as putting the "pyqtree" folder anywhere Python can import it,
such as the folder "PythonXX/Lib/site-packages"

## Example Usage

Start your session by importing the module.

```python
import pyqtree
```

Setup the spatial index, giving it a bounding box area to keep track of.
The bounding box being in a four-tuple: (xmin,ymin,xmax,ymax).

```python
spindex = pyqtree.Index(bbox=[0,0,100,100])
```

Populate the index with items that you want to be retrieved at a later point,
along with each item's geographic bbox.

```python
#this example assumes you have a list of items with bbox attribute
for item in items:
    spindex.insert(item=item, bbox=item.bbox)
```

Then when you have a region of interest and you wish to retrieve items from that region,
just use the index's intersect method. This quickly gives you a list of the stored items
whose bboxes intersects your region of interests. 

```python
overlapbbox = (51,51,86,86)
matches = spindex.intersect(overlapbbox)
```

There are other things that can be done as well, but that's it for the main usage!


## Functions and Classes

### pyqtree.Index(...) --> class object
The top spatial index to be created by the user. Once created it can be
populated with geographically placed members that can later be tested for
intersection with a user inputted geographic bounding box. Note that the
index can be iterated through in a for-statement, which loops through all
all the quad instances and lets you access their properties.

| **option** | **description**
| --- | --- 
| bbox | the coordinate system bounding box of the area that the quadtree should keep track of, as a 4-length sequence (xmin,ymin,xmax,ymax)

  - #### .countmembers(...):
  Returns a count of the total number of members/items/nodes inserted into
  this quadtree and all of its child trees.

  - #### .insert(...):
  Inserts an item into the quadtree along with its bounding box.
  
  | **option** | **description**
  | --- | --- 
  | item | the item to insert into the index, which will be returned by the intersection method
  | bbox | the spatial bounding box tuple of the item, with four members (xmin,ymin,xmax,ymax)

  - #### .intersect(...):
  Intersects an input boundingbox rectangle with all of the items
  contained in the quadtree. Returns a list of items whose bounding
  boxes intersect with the input rectangle.
  
  | **option** | **description**
  | --- | --- 
  | bbox | a spatial bounding box tuple with four members (xmin,ymin,xmax,ymax)
  | results | only used internally

