"""
# Pyqtree

Pyqtree is a pure Python spatial index for GIS or rendering usage.
It stores and quickly retrieves items from a 2x2 rectangular grid area,
and grows in depth and detail as more items are added. 
The actual quad tree implementation is adapted from
[Matt Rasmussen's compbio library](https://github.com/mdrasmus/compbio/blob/master/rasmus/quadtree.py)
and extended for geospatial use.


## Platforms

Python 2 and 3. 


## Dependencies

Pyqtree is written in pure Python and has no dependencies.


## Installing It

Installing Pyqtree can be done by opening your terminal or commandline and typing:

    pip install pyqtree

Alternatively, you can simply download the "pyqtree.py" file and place
it anywhere Python can import it, such as the Python site-packages folder.


## Example Usage

Start your script by importing the module.

    import pyqtree

Setup the spatial index, giving it a bounding box area to keep track of.
The bounding box being in a four-tuple: (xmin,ymin,xmax,ymax).

    spindex = pyqtree.Index(bbox=[0,0,100,100])

Populate the index with items that you want to be retrieved at a later point,
along with each item's geographic bbox.

    # this example assumes you have a list of items with bbox attribute
    for item in items:
        spindex.insert(item=item, bbox=item.bbox)

Then when you have a region of interest and you wish to retrieve items from that region,
just use the index's intersect method. This quickly gives you a list of the stored items
whose bboxes intersects your region of interests. 

    overlapbbox = (51,51,86,86)
    matches = spindex.intersect(overlapbbox)

There are other things that can be done as well, but that's it for the main usage!


## More Information:

- [Home Page](http://github.com/karimbahgat/Pyqtree)
- [API Documentation](http://pythonhosted.org/Pyqtree)


## License:

This code is free to share, use, reuse, and modify according to the MIT license, see LICENSE.txt.


## Credits:

Karim Bahgat (2015)

"""

__version__ = "0.24"

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
        
class _QuadTree:
    """
    Internal backend version of the index.

    The index being used behind the scenes. Has all the same methods as the user
    index, but requires more technical arguments when initiating it than the
    user-friendly version. 

    Args:

    - **x**:
        The x center coordinate of the area that the quadtree should keep track of. 
    - **y**
        The y center coordinate of the area that the quadtree should keep track of.
    - **width**:
        How far from the xcenter that the quadtree should look when keeping track. 
    - **height**:
        How far from the ycenter that the quadtree should look when keeping track
    """
    
    def __init__(self, x, y, width, height, depth=0, maxitems=10, maxdepth=20):
        self.nodes = []
        self.children = []
        self.center = [x, y]
        self.width,self.height = width,height
        self.depth = depth
        self.maxitems = maxitems
        self.maxdepth = maxdepth
        
    def __iter__(self):
        def loopallchildren(parent):
            for child in parent.children:
                if child.children:
                    for subchild in loopallchildren(parent=child):
                        yield subchild
                yield child
        for child in loopallchildren(self):
            yield child
            
    def _insert(self, item, bbox):
        rect = _normalize_rect(bbox)
        if len(self.children) == 0:
            node = _QuadNode(item, rect)
            self.nodes.append(node)
            
            if len(self.nodes) > self.maxitems and self.depth < self.maxdepth:
                self._split()
        else:
            self._insert_into_children(item, rect)
            
    def _intersect(self, bbox, results=None):
        rect = bbox
        if results is None:
            rect = _normalize_rect(rect)
            results = set()
        # search children
        if len(self.children) > 0:
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[0]._intersect(rect, results)
                if rect[3] > self.center[1]:
                    self.children[1]._intersect(rect, results)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2]._intersect(rect, results)
                if rect[3] > self.center[1]:
                    self.children[3]._intersect(rect, results)
        # search node at this level
        for node in self.nodes:
            if (node.rect[2] > rect[0] and node.rect[0] <= rect[2] and 
                node.rect[3] > rect[1] and node.rect[1] <= rect[3]):
                results.add(node.item)
        return results
    
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
                    self.children[0]._insert(item, rect)
                if rect[3] > self.center[1]:
                    self.children[1]._insert(item, rect)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    self.children[2]._insert(item, rect)
                if rect[3] > self.center[1]:
                    self.children[3]._insert(item, rect)
                    
    def _split(self):
        quartwidth = self.width/4.0
        quartheight = self.height/4.0
        halfwidth = self.width/2.0
        halfheight = self.height/2.0
        self.children = [_QuadTree(self.center[0] - quartwidth,
                                  self.center[1] - quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  maxitems=self.maxitems,
                                  maxdepth=self.maxdepth),
                         _QuadTree(self.center[0] - quartwidth,
                                  self.center[1] + quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  maxitems=self.maxitems,
                                  maxdepth=self.maxdepth),
                         _QuadTree(self.center[0] + quartwidth,
                                  self.center[1] - quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  maxitems=self.maxitems,
                                  maxdepth=self.maxdepth),
                         _QuadTree(self.center[0] + quartwidth,
                                  self.center[1] + quartheight,
                                  width=halfwidth, height=halfheight,
                                  depth=self.depth + 1,
                                  maxitems=self.maxitems,
                                  maxdepth=self.maxdepth)]
        nodes = self.nodes
        self.nodes = []
        for node in nodes:
            self._insert_into_children(node.item, node.rect)

#USER CLASSES AND FUNCTIONS
            
class Index(_QuadTree):
    """
    The top spatial index to be created by the user. Once created it can be
    populated with geographically placed members that can later be tested for
    intersection with a user inputted geographic bounding box. Note that the
    index can be iterated through in a for-statement, which loops through all
    all the quad instances and lets you access their properties.
    """
    def __init__(self, bbox, maxitems=10, maxdepth=20):
        """
        Parameters:

        - **bbox**: The coordinate system bounding box of the area that the quadtree should
            keep track of, as a 4-length sequence (xmin,ymin,xmax,ymax)
        - **maxmembers** (optional): The maximum number of items allowed per quad before splitting
            up into four new subquads. Default is 10. 
        - **maxdepth** (optional): The maximum levels of nested subquads, after which no more splitting
            occurs and the bottommost quad nodes may grow indefinately. Default is 20. 
        """
        x1,y1,x2,y2 = bbox
        width,height = x2-x1,y2-y1
        midx,midy = x1+width/2.0, y1+height/2.0
        self.nodes = []
        self.children = []
        self.center = [midx, midy]
        self.width,self.height = width,height
        self.depth = 0
        self.maxitems = maxitems
        self.maxdepth = maxdepth

    def insert(self, item, bbox):
        """
        Inserts an item into the quadtree along with its bounding box.

        Parameters:

        - **item**: The item to insert into the index, which will be returned by the intersection method
        - **bbox**: The spatial bounding box tuple of the item, with four members (xmin,ymin,xmax,ymax)
        """
        self._insert(item, bbox)

    def intersect(self, bbox):
        """
        Intersects an input boundingbox rectangle with all of the items
        contained in the quadtree. 

        Parameters:

        - **bbox**: A spatial bounding box tuple with four members (xmin,ymin,xmax,ymax)

        Returns:

        - A list of inserted items whose bounding boxes intersect with the input rectangle.
        """
        return self._intersect(bbox)
    
    def countmembers(self):
        """
        Returns:
        
        - A count of the total number of members/items/nodes inserted into
            this quadtree and all of its child trees.
        """
        size = 0
        for child in self.children:
            size += child.countmembers()
        size += len(self.nodes)
        return size





