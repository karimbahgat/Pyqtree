# PyQuadTree
A Pure Python QuadTree spatial index for GIS or visualization use
Karim Bahgat, 2014
License: MIT

Based on Matt Rasmussen's original code:
https://github.com/mdrasmus/compbio/blob/master/rasmus/quadtree.py

## Example Usage

First setup and populate the spatial index

```
#assuming you have a list of items with a bounding box attribute
spindex = Index(x=50,y=50,size=45)
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

- __x__  
  the x center coordinate of the area that the quadtree should keep track of
- __y__  
  the y center coordinate of the area that the quadtree should keep track of
- __size__  
  how far from the center (both x and y) that the quadtree should look when keeping track

  - #### .countmembers(...):
  Returns a count of the total number of members/items/nodes inserted into
  this quadtree and all of its child trees.

  - #### .insert(...):
  Inserts an item into the quadtree along with its bounding box.
  
  - __item__  
    the item to insert into the index, which will be returned by the intersection method
  - __bbox__  
    the spatial bounding box tuple of the item, with four members (xmin,ymin,xmax,ymax)

  - #### .intersect(...):
  Intersects an input boundingbox rectangle with all of the items
  contained in the quadtree. Returns a list of items whose bounding
  boxes intersect with the input rectangle.
  
  - __bbox__  
    a spatial bounding box tuple with four members (xmin,ymin,xmax,ymax)
  - __results__  
    only used internally

