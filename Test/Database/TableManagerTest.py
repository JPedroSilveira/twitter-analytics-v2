import unittest
import Test.Helpers.ObjectHelperTest as ObjectHelperTest
from Database.Cons import SupportedTypes

from Database.DBData import DBData
from Database.TableManager import TableManager


class TestPrimitiveClass(DBData):
    def __init__(self):
        return None


class TestPrimitiveTypeClass(DBData):
    int_number = 0
    boolean = True
    float_number = 0.0

    def set_new_values(self, int_number: int, boolean: bool, float_number: float):
        self.int_number = int_number
        self.boolean = boolean
        self.float_number = float_number


class TestComplexTypeClass(DBData):
    int_number = 0
    boolean = True
    float_number = 0.0

    string = ''
    string_size = 10

    list_int = []
    list_int_size = 10
    list_int_type = SupportedTypes.INT_NAME

    list_string = []
    list_string_size = 5
    list_string_type = SupportedTypes.STRING_NAME
    list_string_size_string = 10

    def set_new_values(self, int_number: int, boolean: bool, float_number: float,
                       string: str, list_int: list, list_string: list):
        self.int_number = int_number
        self.boolean = boolean
        self.float_number = float_number
        self.string = string
        self.list_int = list_int
        self.list_string = list_string


class TableManagerTest(unittest.TestCase):

    def test_save_primitive_class_one(self):
        manager = TableManager(TestPrimitiveTypeClass)
        obj = TestPrimitiveTypeClass()
        obj.set_new_values(1, False, 10.0)
        manager.save(obj)

        obj_loaded = manager.find_by_id(obj.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj, obj_loaded))

    def test_save_two_primitive_class(self):
        manager = TableManager(TestPrimitiveTypeClass)

        obj1 = TestPrimitiveTypeClass()
        obj1.set_new_values(1, False, 10.0)
        manager.save(obj1)

        obj2 = TestPrimitiveTypeClass()
        obj2.set_new_values(999, True, 0.0)
        manager.save(obj2)

        obj1_l = manager.find_by_id(obj1.id)
        obj2_l = manager.find_by_id(obj2.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj1_l, obj1))
        self.assertTrue(ObjectHelperTest.compare_objs(obj2_l, obj2))

    def test_save_two_primitive_class_with_different_managers(self):
        manager1 = TableManager(TestPrimitiveTypeClass)

        obj1 = TestPrimitiveTypeClass()
        obj1.set_new_values(1, False, 10.0)
        manager1.save(obj1)

        manager2 = TableManager(TestPrimitiveTypeClass)
        obj2 = TestPrimitiveTypeClass()
        obj2.set_new_values(999, True, 0.0)
        manager2.save(obj2)

        obj1_l = manager2.find_by_id(obj1.id)
        obj2_l = manager1.find_by_id(obj2.id)

        manager1.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj1_l, obj1))
        self.assertTrue(ObjectHelperTest.compare_objs(obj2_l, obj2))

    def test_save_seven_primitive_class(self):
        manager = TableManager(TestPrimitiveTypeClass)

        obj1 = TestPrimitiveTypeClass()
        obj1.set_new_values(1, False, 10.0)

        obj2 = TestPrimitiveTypeClass()
        obj2.set_new_values(999, True, 0.0)

        obj3 = TestPrimitiveTypeClass()
        obj3.set_new_values(99, False, 10.0)

        obj4 = TestPrimitiveTypeClass()
        obj4.set_new_values(991549, False, 56.5)

        obj5 = TestPrimitiveTypeClass()
        obj5.set_new_values(1516, True, 2626.5)

        obj6 = TestPrimitiveTypeClass()
        obj6.set_new_values(2625, True, 3662.26)

        obj7 = TestPrimitiveTypeClass()
        obj7.set_new_values(2525, True, 6269.5)

        manager.save(obj1)
        manager.save(obj2)
        manager.save(obj3)
        manager.save(obj4)
        manager.save(obj5)
        manager.save(obj6)
        manager.save(obj7)

        obj1_l = manager.find_by_id(obj1.id)
        obj2_l = manager.find_by_id(obj2.id)
        obj3_l = manager.find_by_id(obj3.id)
        obj4_l = manager.find_by_id(obj4.id)
        obj5_l = manager.find_by_id(obj5.id)
        obj6_l = manager.find_by_id(obj6.id)
        obj7_l = manager.find_by_id(obj7.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj1_l, obj1))
        self.assertTrue(ObjectHelperTest.compare_objs(obj2_l, obj2))
        self.assertTrue(ObjectHelperTest.compare_objs(obj3_l, obj3))
        self.assertTrue(ObjectHelperTest.compare_objs(obj4_l, obj4))
        self.assertTrue(ObjectHelperTest.compare_objs(obj5_l, obj5))
        self.assertTrue(ObjectHelperTest.compare_objs(obj6_l, obj6))
        self.assertTrue(ObjectHelperTest.compare_objs(obj7_l, obj7))

    def test_delete_primitive_type_class(self):
        manager = TableManager(TestPrimitiveTypeClass)

        obj1 = TestPrimitiveTypeClass()
        obj1.set_new_values(1, False, 10.0)

        obj2 = TestPrimitiveTypeClass()
        obj2.set_new_values(999, True, 0.0)

        obj3 = TestPrimitiveTypeClass()
        obj3.set_new_values(99, False, 10.0)

        manager.save(obj1)
        manager.save(obj2)
        manager.save(obj3)

        manager.delete(obj2)
        manager.delete(obj1)

        obj1_l = manager.find_by_id(obj1.id)
        obj2_l = manager.find_by_id(obj2.id)
        obj3_l = manager.find_by_id(obj3.id)

        manager.drop()

        self.assertEqual(obj1_l, None)
        self.assertEqual(obj2_l, None)
        self.assertTrue(ObjectHelperTest.compare_objs(obj3_l, obj3))

    def test_primitive_class_update(self):
        manager = TableManager(TestPrimitiveTypeClass)

        obj1 = TestPrimitiveTypeClass()
        obj1.set_new_values(1, False, 10.0)

        obj2 = TestPrimitiveTypeClass()
        obj2.set_new_values(999, True, 0.0)

        manager.save(obj1)
        manager.save(obj2)

        obj1.int_number = 976
        obj2.float_number = 26.6
        obj1.boolean = True

        manager.save(obj1)
        manager.save(obj2)

        obj1_l = manager.find_by_id(obj1.id)
        obj2_l = manager.find_by_id(obj2.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj1_l, obj1))
        self.assertTrue(ObjectHelperTest.compare_objs(obj2_l, obj2))

    def test_save_complex_type_with_full_lists(self):
        manager = TableManager(TestComplexTypeClass)

        obj = TestComplexTypeClass()
        obj.set_new_values(20, True, 102.3, 'Teste', [1, 3, 5, 6, 2, 3, 4, 2, 3, 1],
                           ['alskde e e', '          ', 'sdwq sdAS5', '8569856985', 'sdasd$%3as'])

        manager.save(obj)

        obj_l = manager.find_by_id(obj.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj_l, obj))

    def test_save_complex_type_with_empty_lists(self):
        manager = TableManager(TestComplexTypeClass)

        obj = TestComplexTypeClass()
        obj.set_new_values(70, False, 156.59, 'Teste', [], [])

        manager.save(obj)

        obj_l = manager.find_by_id(obj.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj_l, obj))

    def test_save_complex_type_with_empty_string_and_not_full_lists(self):
        manager = TableManager(TestComplexTypeClass)

        obj = TestComplexTypeClass()
        obj.set_new_values(70, False, 156.59, '', [1, 2, 4], ['oiokda sa'])

        manager.save(obj)

        obj_l = manager.find_by_id(obj.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj_l, obj))

    def test_save_complex_type_with_empty_string_and_full_lists(self):
        manager = TableManager(TestComplexTypeClass)

        obj = TestComplexTypeClass()
        obj.set_new_values(70, False, 156.59, '', [1, 3, 5, 6, 2, 3, 4, 2, 3, 1],
                           ['alskde e e', '          ', 'sdwq sdAS5', '8569856985', 'sdasd$%3as'])

        manager.save(obj)

        obj_l = manager.find_by_id(obj.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj_l, obj))

    def test_save_complex_type_with_zero_values(self):
        manager = TableManager(TestComplexTypeClass)

        obj = TestComplexTypeClass()
        obj.set_new_values(0, False, 0.0, '', [], [])

        manager.save(obj)

        obj_l = manager.find_by_id(obj.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj_l, obj))

    def test_save_four_different_complex_type(self):
        manager = TableManager(TestComplexTypeClass)

        obj1 = TestComplexTypeClass()
        obj1.set_new_values(0, False, 0.0, '', [], [])

        obj2 = TestComplexTypeClass()
        obj2.set_new_values(70, False, 156.59, '', [1, 3, 5, 6, 2, 3, 4, 2, 3, 1],
                            ['alskde e e', '          ', 'sdwq sdAS5', '8569856985', 'sdasd$%3as'])

        obj3 = TestComplexTypeClass()
        obj3.set_new_values(698, False, 156.59, '', [1, 2, 4], ['oiokda sa'])

        obj4 = TestComplexTypeClass()
        obj4.set_new_values(250, True, 26266.59, 'LALALA', [1, 6], ['oiokda sa', 'lalaland'])

        manager.save(obj1)
        manager.save(obj2)
        manager.save(obj3)
        manager.save(obj4)

        obj1_l = manager.find_by_id(obj1.id)
        obj2_l = manager.find_by_id(obj2.id)
        obj3_l = manager.find_by_id(obj3.id)
        obj4_l = manager.find_by_id(obj4.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj1_l, obj1))
        self.assertTrue(ObjectHelperTest.compare_objs(obj2_l, obj2))
        self.assertTrue(ObjectHelperTest.compare_objs(obj3_l, obj3))
        self.assertTrue(ObjectHelperTest.compare_objs(obj4_l, obj4))

    def test_save_four_different_complex_type_and_update_two(self):
        manager = TableManager(TestComplexTypeClass)

        obj1 = TestComplexTypeClass()
        obj1.set_new_values(0, False, 0.0, '', [], [])

        obj2 = TestComplexTypeClass()
        obj2.set_new_values(70, False, 156.59, '', [1, 3, 5, 6, 2, 3, 4, 2, 3, 1],
                            ['alskde e e', '          ', 'sdwq sdAS5', '8569856985', 'sdasd$%3as'])

        obj3 = TestComplexTypeClass()
        obj3.set_new_values(698, False, 156.59, '', [1, 2, 4], ['oiokda sa'])

        obj4 = TestComplexTypeClass()
        obj4.set_new_values(250, True, 26266.59, 'LALALA', [1, 6], ['oiokda sa', 'lalaland'])

        manager.save(obj1)
        manager.save(obj2)
        manager.save(obj3)
        manager.save(obj4)

        obj1_l = manager.find_by_id(obj1.id)
        obj2_l = manager.find_by_id(obj2.id)
        obj3_l = manager.find_by_id(obj3.id)
        obj4_l = manager.find_by_id(obj4.id)

        obj2_l.list_string = []
        obj2_l.list_int = [0]
        obj2_l.number = 20
        obj2_l.boolean = True
        obj3_l.list_string = ['alskde e e', '          ', 'sdwq sdAS5', '8569856985', 'sdasd$%3as']
        obj3_l.list_int = [1, 3, 5, 6, 2, 3, 4, 2, 3, 1]
        obj3_l.string = 'laeio'
        obj3_l.number = 0
        obj3_l.float_number = 25.2

        manager.save(obj3_l)
        manager.save(obj2_l)

        obj2_r_l = manager.find_by_id(obj2_l.id)
        obj3_r_l = manager.find_by_id(obj3_l.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj1_l, obj1))
        self.assertTrue(ObjectHelperTest.compare_objs(obj2_r_l, obj2_l))
        self.assertTrue(ObjectHelperTest.compare_objs(obj3_r_l, obj3_l))
        self.assertTrue(ObjectHelperTest.compare_objs(obj4_l, obj4))

    def test_save_four_different_complex_type_and_update_two_and_delete_two(self):
        manager = TableManager(TestComplexTypeClass)

        obj1 = TestComplexTypeClass()
        obj1.set_new_values(0, False, 0.0, '', [], [])

        obj2 = TestComplexTypeClass()
        obj2.set_new_values(70, False, 156.59, '', [1, 3, 5, 6, 2, 3, 4, 2, 3, 1],
                            ['alskde e e', '          ', 'sdwq sdAS5', '8569856985', 'sdasd$%3as'])

        obj3 = TestComplexTypeClass()
        obj3.set_new_values(698, False, 156.59, '', [1, 2, 4], ['oiokda sa'])

        obj4 = TestComplexTypeClass()
        obj4.set_new_values(250, True, 26266.59, 'LALALA', [1, 6], ['oiokda sa', 'lalaland'])

        manager.save(obj1)
        manager.save(obj2)
        manager.save(obj3)
        manager.save(obj4)

        obj1_l = manager.find_by_id(obj1.id)
        obj2_l = manager.find_by_id(obj2.id)
        obj3_l = manager.find_by_id(obj3.id)
        obj4_l = manager.find_by_id(obj4.id)

        obj2_l.list_string = []
        obj2_l.list_int = [0]
        obj2_l.number = 20
        obj2_l.boolean = True
        obj3_l.list_string = ['alskde e e', '          ', 'sdwq sdAS5', '8569856985', 'sdasd$%3as']
        obj3_l.list_int = [1, 3, 5, 6, 2, 3, 4, 2, 3, 1]
        obj3_l.string = 'laeio'
        obj3_l.number = 0
        obj3_l.float_number = 25.2

        manager.save(obj3_l)
        manager.save(obj2_l)
        manager.delete(obj1_l)
        manager.delete(obj4_l)

        obj2_r_l = manager.find_by_id(obj2_l.id)
        obj3_r_l = manager.find_by_id(obj3_l.id)
        obj1_r_l = manager.find_by_id(obj1_l.id)
        obj4_r_l = manager.find_by_id(obj4_l.id)

        manager.drop()

        self.assertTrue(ObjectHelperTest.compare_objs(obj3_r_l, obj3_l))
        self.assertTrue(ObjectHelperTest.compare_objs(obj2_r_l, obj2_l))
        self.assertEqual(obj1_r_l, None)
        self.assertEqual(obj4_r_l, None)


if __name__ == '__main__':
    unittest.main()
