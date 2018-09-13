
import pyqtree
import random, time

class Item:
    def __init__(self, x, y):
        left = x-1
        right = x+1
        top = y-1
        bottom = y+1
        self.bbox = [left,top,right,bottom]

#setup and populate index
items = [Item(random.randrange(5,95),random.randrange(5,95)) for _ in range(10000)]
spindex = pyqtree.Index(bbox=[-11,-33,100,100])
for item in items:
    spindex.insert(item, item.bbox)
print("{0} members in this index.".format(len(spindex)))

#test intersection
print("testing hit")
testitem = (51,51,86,86)
t = time.time()
matches = spindex.intersect(testitem)
print("{0} seconds".format(time.time()-t))

#test countmembers()
# trivial list of items
items = [Item(0.5, 0.5), Item(-0.5, 0.5), Item(-0.5, -0.5), Item(0.5, -0.5)]

# populate: maxindex=3, so we must split
spindex = pyqtree.Index(bbox=[-1, -1, 1, 1], max_items=3)
for item in items:
    spindex.insert(item, item.bbox)

# check result
members = len(spindex)
assert(members == 4)
print("{0} nodes in this Index.".format(members))

