import character_data
import object_data
import entity_data
import unique_id_data

import unittest

class TestCharacter(unittest.TestCase):
  def test_character(self):
    char = character_data.character_data()

    char.name = "bob"
    char.desc = "<p>This is Bob.</p>"
    char.ldesc = "Bob is standing around."
    char.room = unique_id_data.unique_id_data("stockville", "casino")
    char.reset_aliases("bob", "nice")

    self.assertEqual(char.name, "bob")
    self.assertEqual(char.Name, "Bob")
    self.assertEqual(char.desc, "<p>This is Bob.</p>")
    self.assertEqual(char.ldesc, "Bob is standing around.")
    self.assertEqual(str(char.room), "stockville[casino]")
    self.assertEqual(char.room.zone_id, "stockville")
    self.assertEqual(char.room.id, "casino")
    self.assertEqual(char.in_zone, "stockville")
    self.assertTrue(char.has_alias("bob"))
    self.assertTrue(char.has_alias("nice"))
    self.assertFalse(char.has_alias("notmyname"))

    char.write("This should trigger a warning, but not raise an exception.")

    self.assertEqual(str(char), char.name)

    print(char.debug())

  def test_inventory(self):
    char = character_data.character_data()
    obj1 = object_data.object_data()
    obj2 = object_data.object_data()
    obj3 = object_data.object_data()

    char.give_object(obj1)
    char.give_object(obj2)

    self.assertTrue(char.has_object(obj1))
    self.assertTrue(char.has_object(obj2))

    self.assertFalse(char.has_object(obj3))

    char.give_object(obj3)

    self.assertEqual(char.inventory(), [obj1, obj2, obj3])

    char.lose_object(obj1)

    self.assertFalse(char.has_object(obj1))
    self.assertEqual(char.inventory(), [obj2, obj3])

  def test_copy_transfer(self):
    char = character_data.character_data()
    char.name = "bob"
    char.desc = "<p>This is Bob.</p>"
    char.ldesc = "Bob is standing around."
    char.room = unique_id_data.unique_id_data("stockville", "casino")
    char.reset_aliases("bob", "nice")

    obj1 = object_data.object_data()
    obj2 = object_data.object_data()

    char.give_object(obj1)
    char.give_object(obj2)

    char2 = character_data.character_data()


    char2.copy_from(char)

    self.assertEqual(char.name, char2.name)
    self.assertEqual(char.desc, char2.desc)
    self.assertEqual(char.ldesc, char2.ldesc)

    char.transfer_obj(obj1, char2)

    self.assertFalse(char.has_object(obj1))
    self.assertTrue(char2.has_object(obj1))

    char.transfer_obj(obj2, char2)

    self.assertFalse(char.has_object(obj2))
    self.assertTrue(char2.has_object(obj2))

    char2.transfer_inventory(char)
    self.assertFalse(char2.has_object(obj1))
    self.assertFalse(char2.has_object(obj2))
    self.assertTrue(char.has_object(obj1))
    self.assertTrue(char.has_object(obj2))
    
if __name__ == "__main__":
  unittest.main()