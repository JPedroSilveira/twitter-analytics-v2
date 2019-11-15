import unittest

from Database.DBData import DBData
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNode50String, BTreeNodeInt, BTreeNode
from Database.TableManager import TableManager

_TEST_DEGREE = 3


class TestIntClass(DBData):
    external_id = 0

    def __init__(self, external_id: int):
        self.external_id = external_id


class TestStringClass(DBData):
    unique_name = ''
    unique_name_size = 50

    def __init__(self, unique_name: str):
        self.unique_name = unique_name


# Node with integer keys
class BTreeNode50StringTest(BTreeNode50String):
    # Defines the sized based in the degree
    children_ids_size = _TEST_DEGREE
    keys_size = _TEST_DEGREE - 1
    contents_size = _TEST_DEGREE - 1

    def __init__(self):
        self.children_ids = []
        self.keys = []
        self.contents = []


# Node with integer keys
class BTreeNodeIntTest(BTreeNodeInt):
    # Defines the sized based in the degree
    children_ids_size = _TEST_DEGREE
    keys_size = _TEST_DEGREE - 1
    contents_size = _TEST_DEGREE - 1

    def __init__(self):
        self.children_ids = []
        self.keys = []
        self.contents = []


class BTreeTest(unittest.TestCase):

    def test_btree_with_two_int_values(self):
        manager = TableManager(TestIntClass)
        btree = BTree('external_id', BTreeNodeIntTest, TestIntClass)

        obj1 = TestIntClass(927803)
        obj2 = TestIntClass(92716)

        manager.save(obj1)
        manager.save(obj2)

        btree.insert(obj1.external_id, obj1.id)
        btree.insert(obj2.external_id, obj2.id)

        obj1_id = btree.search(obj1.external_id)
        obj2_id = btree.search(obj2.external_id)

        manager.drop()

        self.assertEqual(obj1.id, obj1_id)
        self.assertEqual(obj2.id, obj2_id)

    def test_btree_with_two_string_values(self):
        manager = TableManager(TestStringClass)
        btree = BTree('unique_name', BTreeNode50StringTest, TestStringClass)

        obj1 = TestStringClass('fulano_id')
        obj2 = TestStringClass('ciclano_id')

        manager.save(obj1)
        manager.save(obj2)

        btree.insert(obj1.unique_name, obj1.id)
        btree.insert(obj2.unique_name, obj2.id)

        obj1_id = btree.search(obj1.unique_name)
        obj2_id = btree.search(obj2.unique_name)

        manager.drop()

        self.assertEqual(obj1.id, obj1_id)
        self.assertEqual(obj2.id, obj2_id)

    def test_btree_int_with_three_values(self):
        manager = TableManager(TestIntClass)
        btree = BTree('external_id', BTreeNodeIntTest, TestIntClass)

        obj1 = TestIntClass(927803)
        obj2 = TestIntClass(92716)
        obj3 = TestIntClass(523)

        manager.save(obj1)
        manager.save(obj2)
        manager.save(obj3)

        btree.insert(obj1.external_id, obj1.id)
        btree.insert(obj2.external_id, obj2.id)
        btree.insert(obj3.external_id, obj3.id)

        obj1_id = btree.search(obj1.external_id)
        obj2_id = btree.search(obj2.external_id)
        obj3_id = btree.search(obj3.external_id)

        manager.drop()

        self.assertEqual(obj1.id, obj1_id)
        self.assertEqual(obj2.id, obj2_id)
        self.assertEqual(obj3.id, obj3_id)

    def test_btree_int_with_ten_values(self):
        manager = TableManager(TestIntClass)
        btree = BTree('external_id', BTreeNodeIntTest, TestIntClass)

        obj1 = TestIntClass(927803)
        obj2 = TestIntClass(92716)
        obj3 = TestIntClass(523)
        obj4 = TestIntClass(5233)
        obj5 = TestIntClass(55)
        obj6 = TestIntClass(51)
        obj7 = TestIntClass(5)
        obj8 = TestIntClass(52563)
        obj9 = TestIntClass(98989)
        obj10 = TestIntClass(335)

        manager.save(obj1)
        manager.save(obj2)
        manager.save(obj3)
        manager.save(obj4)
        manager.save(obj5)
        manager.save(obj6)
        manager.save(obj7)
        manager.save(obj8)
        manager.save(obj9)
        manager.save(obj10)

        btree.insert(obj1.external_id, obj1.id)
        btree.insert(obj2.external_id, obj2.id)
        btree.insert(obj3.external_id, obj3.id)
        btree.insert(obj4.external_id, obj4.id)
        btree.insert(obj5.external_id, obj5.id)
        btree.insert(obj6.external_id, obj6.id)
        btree.insert(obj7.external_id, obj7.id)
        btree.insert(obj8.external_id, obj8.id)
        btree.insert(obj9.external_id, obj9.id)
        btree.insert(obj10.external_id, obj10.id)

        obj1_id = btree.search(obj1.external_id)
        obj2_id = btree.search(obj2.external_id)
        obj3_id = btree.search(obj3.external_id)
        obj4_id = btree.search(obj4.external_id)
        obj5_id = btree.search(obj5.external_id)
        obj6_id = btree.search(obj6.external_id)
        obj7_id = btree.search(obj7.external_id)
        obj8_id = btree.search(obj8.external_id)
        obj9_id = btree.search(obj9.external_id)
        obj10_id = btree.search(obj10.external_id)

        manager.drop()

        self.assertEqual(obj1.id, obj1_id)
        self.assertEqual(obj2.id, obj2_id)
        self.assertEqual(obj3.id, obj3_id)
        self.assertEqual(obj4.id, obj4_id)
        self.assertEqual(obj5.id, obj5_id)
        self.assertEqual(obj6.id, obj6_id)
        self.assertEqual(obj7.id, obj7_id)
        self.assertEqual(obj8.id, obj8_id)
        self.assertEqual(obj9.id, obj9_id)
        self.assertEqual(obj10.id, obj10_id)

    def test_btree_int_with_ten_consecutive_values(self):
        manager = TableManager(TestIntClass)
        btree = BTree('external_id', BTreeNodeIntTest, TestIntClass)

        obj_list = []

        for x in range(590, 600):
            obj = TestIntClass(x)
            manager.save(obj)
            btree.insert(obj.external_id, obj.id)
            obj_list.append(obj)

        for obj in obj_list:
            obj_id = btree.search(obj.external_id)
            self.assertEqual(obj.id, obj_id)

        manager.drop()

    def test_btree_int_with_sixteen_consecutive_values(self):
        manager = TableManager(TestIntClass)
        btree = BTree('external_id', BTreeNodeIntTest, TestIntClass)

        obj_list = []

        for x in range(590, 606):
            obj = TestIntClass(x)
            manager.save(obj)
            btree.insert(obj.external_id, obj.id)
            obj_list.append(obj)

        for obj in obj_list:
            obj_id = btree.search(obj.external_id)
            self.assertEqual(obj.id, obj_id)

        manager.drop()

    def test_btree_int_with_one_hundred_consecutive_values(self):
        manager = TableManager(TestIntClass)
        btree = BTree('external_id', BTreeNodeIntTest, TestIntClass)

        obj_list = []

        for x in range(0, 100):
            obj = TestIntClass(x)
            manager.save(obj)
            btree.insert(obj.external_id, obj.id)
            obj_list.append(obj)

        for obj in obj_list:
            obj_id = btree.search(obj.external_id)
            self.assertEqual(obj.id, obj_id)

        manager.drop()

    def test_btree_string_with_sixteen_string_values(self):
        manager = TableManager(TestStringClass)
        btree = BTree('unique_name', BTreeNode50StringTest, TestStringClass)

        obj_list = []
        unique_name_list = ['fulado', 'ciclano', 'jorge', 'testador', 'carinha que mora logo ali', 'taison', 'felipe',
                            'seu jorge', 'nao olha pro meu teste', 'mesme', 'pouye', 'odia', 'treze', 'quatorze',
                            'tiaos', 'finalmente']

        for x in range(0, 16):
            obj = TestStringClass(unique_name_list[x])
            manager.save(obj)
            btree.insert(obj.unique_name, obj.id)
            obj_list.append(obj)

        for obj in obj_list:
            obj_id = btree.search(obj.unique_name)
            self.assertEqual(obj.id, obj_id)

        manager.drop()

    def test_btree_int_update_with_sixteen_consecutive_values(self):
        manager = TableManager(TestIntClass)
        btree = BTree('external_id', BTreeNodeIntTest, TestIntClass)

        obj_list = []

        for x in range(590, 606):
            obj = TestIntClass(x)
            manager.save(obj)
            btree.insert(obj.external_id, obj.id)
            obj_list.append(obj)

        # Fake change of id
        count = 10
        for obj in obj_list:
            obj.id = count
            btree.insert(obj.external_id, obj.id)
            count = count + 1

        for obj in obj_list:
            obj_id = btree.search(obj.external_id)
            self.assertEqual(obj.id, obj_id)

        manager.drop()


if __name__ == '__main__':
    unittest.main()
