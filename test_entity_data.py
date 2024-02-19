import entity_data
import entity_proto_data
import unittest

class TestEntity(unittest.TestCase):
  def test_entity(self):
    ent = entity_data.entity_data()

    ent.name = "a young dog"
    ent.namelist = ["dog", "young", "young"]
    ent.ldesc = "A young dog chases after a ball."
    ent.desc = "<p>It looks like a young puppy.</p>"

    self.assertTrue(ent.has_alias("young"))
    self.assertTrue(ent.has_alias("dog"))
    self.assertFalse(ent.has_alias("cat"))
    self.assertEqual(ent.namelist, ["dog", "young"])
    self.assertEqual(ent.Name, "A young dog")
    self.assertEqual(ent.ldesc, "A young dog chases after a ball.")
    self.assertEqual(ent.desc, "<p>It looks like a young puppy.</p>")
    self.assertEqual(ent.room, None)

if __name__ == "__main__":
  unittest.main()