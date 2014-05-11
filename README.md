# PyQuadTree

A pure Python QuadTree spatial index for GIS or rendering usage.

Karim Bahgat, 2014

License: MIT

Based on Matt Rasmussen's original code:
https://github.com/mdrasmus/compbio/blob/master/rasmus/quadtree.py

## Installing It

Installing PyQuadTree is as easy as putting the "pyqtree" folder anywhere Python can import it,
such as the folder "PythonXX/Lib/site-packages"

## Example Usage

Setup and populate the spatial index

```
#assuming you have a list of items with a bounding box attribute
import pyqtree
spindex = pyqtree.Index(x=50,y=50,size=45)
for item in items:
    spindex.insert(item=item, bbox=item.bbox)
```

Then retrieve index items that overlap a queried bounding box area

```
overlapbbox = (51,51,86,86)
matches = spindex.intersect(overlapbbox)
```


## Functions and Classes

### pyqtree.Index(...) --> class object
The top spatial index to be created by the user. Once created it can be
populated with geographically placed members that can later be tested for
intersection with a user inputted geographic bounding box.

| **option** | **description**
| --- | --- 
| x | the x center coordinate of the area that the quadtree should keep track of
| y | the y center coordinate of the area that the quadtree should keep track of
| size | how far from the center (both x and y) that the quadtree should look when keeping track

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

