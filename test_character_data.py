import character_data
import editor
import entity_data
import unittest
import unique_id_data

class TestCharacter(unittest.TestCase):
  def test_character(self):
    char = character_data.character_data()

    char.name = "bob"
    char.desc = editor.buffer("<p>This is Bob.  Bob is nice.  Be like Bob.</p>")
    char.ldesc = "Bob is standing around."
    char.room = unique_id_data.unique_id_data("stockville", "casino")
    char.namelist = ["bob", "nice"]

    self.assertEqual(char.name, "bob")
    self.assertEqual(char.Name, "Bob")
    self.assertEqual(type(char.desc), editor.buffer)
    self.assertEqual(char.ldesc, "Bob is standing around.")
    self.assertEqual(str(char.room), "stockville[casino]")
    self.assertEqual(char.room.zone_id, "stockville")
    self.assertEqual(char.room.id, "casino")
    self.assertEqual(char.in_zone, "stockville")
    self.assertTrue(char.has_alias("bob"))
    self.assertTrue(char.has_alias("nice"))

    # I'm essentially testing the @entity.setter here
    # does this go outside the scope of a unit test?
    entity = entity_data.entity_data()
    entity.name = "terry"
    entity.namelist = ["terry", "mean"]
    entity.ldesc = "Terry is standing here."
    entity.desc = editor.buffer("<p>This is Terry.  Terry is mean.  Don't be like Terry.</p>")
    entity.room = unique_id_data.unique_id_data("newbie_zone", "hallway")
    char.entity = entity

    # assuming entity getters are correct, tested in test_entity_data.py
    self.assertEqual(char.name, entity.name)
    self.assertEqual(char.Name, entity.Name)
    self.assertEqual(char.ldesc, entity.ldesc)
    self.assertEqual(char.desc, entity.desc)
    self.assertEqual(char.room, entity.room)

    char.write("This should trigger a warning, but not raise an exception.")

    self.assertTrue(char.has_alias("terry"))
    self.assertTrue(char.has_alias("mean"))

    self.assertEqual(str(char), char.name)

    print(char.debug())
if __name__ == "__main__":
  unittest.main()