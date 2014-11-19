"""
PyQuadTree

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

"""

#PYTHON VERSION CHECK
import sys
PYTHON3 = int(sys.version[0]) == 3
if PYTHON3:
    xrange = range

#INTERNAL USE ONLY
def _normalize_rect(rect):
    x1, y1, x2, y2 = rect
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return (x1, y1, x2, y2)

class _QuadNode:    
    def __init__(self, item, rect):
        self.item = item
        self.rect = rect
        
class _Index:
    """
    The index being used behind the scenes. Has all the same methods as the user
    index, but requires more technical arguments when initiating it than the
    user-friendly version. 

    | **option** | **description**
    | --- | --- 
    | x | the x center coordinate of the area that the quadtree should keep track of
    | y | the y center coordinate of the area that the quadtree should keep track of
    | width | how far from the xcenter that the quadtree should look when keeping track
    | height | how far from the ycenter that the quadtree should look when keeping track

    """
    MAX = 10
    MAX_DEPTH = 20
    def __init__(self, x, y, width, height, depth = 0):
        self.nodes = []
        self.children = []
        self.center = [x, y]
        self.width,self.height = width,height
        self.depth = depth
    def __iter__(self):
        def loopallchildren(parent):
            for child in parent.children:
                if child.children:
                    for subchild in loopallchildren(parent=child):
                        yield subchild
                yield child
        for child in loopallchildren(self):
            yield child
    def insert(self, item, bbox):
        """
        Inserts an item into the quadtree along with its bounding box.

        | **option** | **description**
        | --- | --- 
        | item | the item to insert into the index, which will be returned by the intersection method
        | bbox | the spatial bounding box tuple of the item, with four members (xmin,ymin,xmax,ymax)
        """
        rect = _normalize_rect(bbox)
        if len(self.children) == 0:
            node = _QuadNode(item, rect)
            self.nodes.append(node)
            
            if len(self.nodes) > self.MAX and self.depth < self.MAX_DEPTH:
                self._split()
        else:
            self._insert_into_children(item, rect)
    def intersect(self, bbox, results=None):
        """
        Intersects an input boundingbox rectangle with all of the items
        contained in the quadtree. Returns a list of items whose bounding
        boxes intersect with the input rectangle.

        | **option** | **description**
        | --- | --- 
        | bbox | a spatial bounding box tuple with four members (xmin,ymin,xmax,ymax)
        | results | only used internally
        """
        rect = bbox
        if results is None:
            rect = _normalize_rect(rect)
            results = set()
        # search children
        if len(self.children) > 0:
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0].intersect(rect, results)
                if rect[3] > self.center[1]:
                    self.children[1].intersect(rect, results)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2].intersect(rect, results)
                if rect[3] > self.center[1]:
                    self.children[3].intersect(rect, results)
        # search node at this level
        for node in self.nodes:
            if (node.rect[2] > rect[0] and node.rect[0] <= rect[2] and 
                node.rect[3] > rect[1] and node.rect[1] <= rect[3]):
                results.add(node.item)
        return results
    def countmembers(self):
        """
        Returns a count of the total number of members/items/nodes inserted into
        this quadtree and all of its child trees.
        """
        size = 0
        for child in self.children:
            size += child.countmembers()
        size += len(self.nodes)
        return size
    
    #INTERNAL USE ONLY
    def _insert_into_children(self, item, rect):
        # if rect spans center then insert here
        if ((rect[0] <= self.center[0] and rect[2] > self.center[0]) and
            (rect[1] <= self.center[1] and rect[3] > self.center[1])):
            node = _QuadNode(item, rect)
            self.nodes.append(node)
        else:
            # try to insert into children
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0].insert(item, rect)
                if rect[3] > self.center[1]:
                    self.children[1].insert(item, rect)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2].insert(item, rect)
                if rect[3] > self.center[1]:
                    self.children[3].insert(item, rect)
    def _split(self):
        quartwidth = self.width/4.0
        quartheight = self.height/4.0
        halfwidth = self.width/2.0
        halfheight = self.height/2.0
        self.children = [_Index(self.center[0] - quartwidth,
                                  self.center[1] - quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1),
                         _Index(self.center[0] - quartwidth,
                                  self.center[1] + quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1),
                         _Index(self.center[0] + quartwidth,
                                  self.center[1] - quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1),
                         _Index(self.center[0] + quartwidth,
                                  self.center[1] + quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1)]
        nodes = self.nodes
        self.nodes = []
        for node in nodes:
            self._insert_into_children(node.item, node.rect)

#USER CLASSES AND FUNCTIONS 
class Index(_Index):
    """
    The top spatial index to be created by the user. Once created it can be
    populated with geographically placed members that can later be tested for
    intersection with a user inputted geographic bounding box. Note that the
    index can be iterated through in a for-statement, which loops through all
    all the quad instances and lets you access their properties.

    | **option** | **description**
    | --- | --- 
    | bbox | the coordinate system bounding box of the area that the quadtree should keep track of, as a 4-length sequence (xmin,ymin,xmax,ymax)
    
    """
    def __init__(self, bbox):
        x1,y1,x2,y2 = bbox
        width,height = x2-x1,y2-y1
        midx,midy = x1+width/2.0, y1+height/2.0
        self.nodes = []
        self.children = []
        self.center = [midx, midy]
        self.width,self.height = width,height
        self.depth = 0

#SOME TESTING
if __name__ == "__main__":
    import random, time
    
    class Item:
        def __init__(self, x, y):
            left = x-1
            right = x+1
            top = y-1
            bottom = y+1
            self.bbox = [left,top,right,bottom]

    #setup and populate index
    items = [Item(random.randrange(5,95),random.randrange(5,95)) for _ in xrange(1000)]
    spindex = Index(bbox=[-11,-33,100,100])
    for item in items:
        spindex.insert(item, item.bbox)

    #test intersection
    print("testing hit")
    testitem = (51,51,86,86)
    t = time.time()
    matches = spindex.intersect(testitem)
    print(time.time()-t, " seconds")

