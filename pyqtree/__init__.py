"""

Pure Python QuadTree spatial index for GIS use
Karim Bahgat, 2014

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

"""

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

#USER CLASSES AND FUNCTIONS
class Index:
    """
    The top spatial index to be created by the user. Once created it can be
    populated with geographically placed members that can later be tested for
    intersection with a user inputted geographic bounding box.

    - __x__  
      the x center coordinate of the area that the quadtree should keep track of
    - __y__  
      the y center coordinate of the area that the quadtree should keep track of
    - __size__  
      how far from the center (both x and y) that the quadtree should look when keeping track
    """
    MAX = 10
    MAX_DEPTH = 20
    def __init__(self, x, y, size, depth = 0):
        self.nodes = []
        self.children = []
        self.center = [x, y]
        self.size = size
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

        - __item__  
          the item to insert into the index, which will be returned by the intersection method
        - __bbox__  
          the spatial bounding box tuple of the item, with four members (xmin,ymin,xmax,ymax)
        """
        rect = _normalize_rect(bbox)
        if len(self.children) == 0:
            node = _QuadNode(item, rect)
            self.nodes.append(node)
            
            if len(self.nodes) > self.MAX and self.depth < self.MAX_DEPTH:
                self._split()
                return node
        else:
            return self._insert_into_children(item, rect)
    def intersect(self, bbox, results=None):
        """
        Intersects an input boundingbox rectangle with all of the items
        contained in the quadtree. Returns a list of items whose bounding
        boxes intersect with the input rectangle.

        - __bbox__  
          a spatial bounding box tuple with four members (xmin,ymin,xmax,ymax)
        - __results__  
          only used internally
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
            return node
        else:
            # try to insert into children
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    return self.children[0].insert(item, rect)
                if rect[3] > self.center[1]:
                    return self.children[1].insert(item, rect)
            if rect[2] > self.center[0]:
                if rect[1] <= self.center[1]:
                    return self.children[2].insert(item, rect)
                if rect[3] > self.center[1]:
                    return self.children[3].insert(item, rect)
    def _split(self):
        self.children = [Index(self.center[0] - self.size/2,
                                  self.center[1] - self.size/2,
                                  self.size/2, self.depth + 1),
                         Index(self.center[0] - self.size/2,
                                  self.center[1] + self.size/2,
                                  self.size/2, self.depth + 1),
                         Index(self.center[0] + self.size/2,
                                  self.center[1] - self.size/2,
                                  self.size/2, self.depth + 1),
                         Index(self.center[0] + self.size/2,
                                  self.center[1] + self.size/2,
                                  self.size/2, self.depth + 1)]
        nodes = self.nodes
        self.nodes = []
        for node in nodes:
            self._insert_into_children(node.item, node.rect)


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
    spindex = Index(50,50,45)
    for item in items:
        spindex.insert(item, item.bbox)

    #test intersection
    print "testing hit"
    testitem = (51,51,86,86)
    t = time.time()
    matches = spindex.intersect(testitem)
    print time.time()-t, " seconds"

