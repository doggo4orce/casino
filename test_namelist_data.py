import namelist_data
import unittest

class TestNamelist(unittest.TestCase):
  def test_namelist(self):
    test_namelist1 = namelist_data.namelist_data("dog", "young", "puppy")
    test_namelist2 = namelist_data.namelist_data("cat", "old")

    self.assertTrue(test_namelist1.has_alias("young"))
    self.assertTrue(test_namelist1.has_alias("dog"))
    self.assertTrue(test_namelist1.has_alias("puppy"))
    self.assertFalse(test_namelist1.has_alias("hound"))

    test_namelist1.remove_alias("dog")
    self.assertFalse(test_namelist1.has_alias("dog"))

    self.assertTrue(test_namelist2.has_alias("cat"))
    self.assertTrue(test_namelist2.has_alias("old"))
    self.assertFalse(test_namelist2.has_alias("tabby"))

  def test_iterator(self):
    keywords = [
      "some",
      "very",
      "nice",
      "name"
    ]

    test_namelist = namelist_data.namelist_data(*keywords)

    print(test_namelist)

    for idx, word in enumerate(keywords):
      self.assertTrue(test_namelist.has_alias(word))
      self.assertEqual(test_namelist[idx], keywords[idx])

    for idx, word in enumerate(test_namelist):
      self.assertEqual(keywords[idx], test_namelist[idx])

    self.assertEqual(test_namelist.num_aliases, 4)

    test_namelist.remove_alias("very")

    # remove this, there is no reason for it
    self.assertEqual(test_namelist[0], keywords[0])
    self.assertEqual(test_namelist[1], keywords[2])
    self.assertEqual(test_namelist[2], keywords[3])
    
    self.assertFalse(test_namelist.has_alias("very"))

    test_namelist.remove_all()
    self.assertEqual(test_namelist.num_aliases, 0)

  def test_reset(self):
    keywords = [
      "some",
      "very",
      "nice",
      "name"
    ]

    tn = namelist_data.namelist_data("remove", "this")

    tn.reset(*keywords)

    self.assertEqual(tn.num_aliases, 4)

    for word in keywords:
      self.assertTrue(tn.has_alias(word))

    print(tn)

  def test_list(self):
    keywords = [
      "some",
      "very",
      "nice",
      "name"
    ]

    tn = namelist_data.namelist_data(*keywords)

    names = tn.list()

    for keyword in keywords:
      self.assertIn(keyword, names)

    names.remove("nice")

    self.assertTrue(tn.has_alias("nice"))

if __name__ == "__main__":
  unittest.main()