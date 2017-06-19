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

def test_should_empty_index_after_removing_added_node():
    index = Index(INDEX_BBOX)
    index.insert(ITEM1, BBOX1)
    index.remove(ITEM1, BBOX1)
    assert len(index) == 0
    assert index.intersect(BBOX1) == set()

def test_should_empty_index_after_removing_multiple_added_nodes_in_separate_quad_nodes():
    index = Index(INDEX_BBOX, max_items=1)
    index.insert(ITEM1, BBOX1)
    index.insert(ITEM2, BBOX2)
    index.remove(ITEM1, BBOX1)
    index.remove(ITEM2, BBOX2)
    assert len(index) == 0
    assert index.intersect(INDEX_BBOX) == set()

def test_should_empty_index_after_removing_multiple_added_nodes_in_all_quad_nodes():
    index = Index(INDEX_BBOX, max_items=1)
    index.insert(ITEM1, BBOX1)
    index.insert(ITEM2, INDEX_BBOX)
    index.remove(ITEM1, BBOX1)
    index.remove(ITEM2, INDEX_BBOX)
    assert len(index) == 0
    assert index.intersect(INDEX_BBOX) == set()

def test_should_empty_index_after_removing_multiple_added_nodes_in_multiple_horizontal_quad_nodes():
    index = Index(INDEX_BBOX, max_items=1)
    bbox2 = (0, 0, INDEX_BBOX[2], 1)
    index.insert(ITEM1, BBOX1)
    index.insert(ITEM2, bbox2)
    index.remove(ITEM1, BBOX1)
    index.remove(ITEM2, bbox2)
    assert len(index) == 0
    assert index.intersect(INDEX_BBOX) == set()

def test_should_empty_index_after_removing_multiple_added_nodes_in_multiple_vertical_quad_nodes():
    index = Index(INDEX_BBOX, max_items=1)
    bbox2 = (0, 0, 1, INDEX_BBOX[3])
    index.insert(ITEM1, BBOX1)
    index.insert(ITEM2, bbox2)
    index.remove(ITEM1, BBOX1)
    index.remove(ITEM2, bbox2)
    assert len(index) == 0
    assert index.intersect(INDEX_BBOX) == set()
