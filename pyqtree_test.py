from pyqtree import Index

INDEX_BBOX = (0, 0, 10, 10)

ITEM1 = 'Item 1'
BBOX1 = (0, 0, 0, 0)

ITEM2 = 'Item 2'
BBOX2 = (1, 1, 1, 1)


def test_should_initially_count_zero_members():
    index = Index(INDEX_BBOX)
    assert len(index) == 0

def test_should_add_single_node_and_find_its_intersection():
    index = Index(INDEX_BBOX)
    index.insert(ITEM1, BBOX1)
    assert len(index) == 1
    assert index.intersect(BBOX1) == {ITEM1}

def test_should_add_multiple_nodes_and_find_them():
    index = Index(INDEX_BBOX)
    index.insert(ITEM1, BBOX1)
    index.insert(ITEM2, BBOX2)
    assert len(index) == 2
    assert index.intersect(BBOX1) == {ITEM1}
    assert index.intersect(BBOX2) == {ITEM2}
    assert index.intersect(INDEX_BBOX) == {ITEM1, ITEM2}
