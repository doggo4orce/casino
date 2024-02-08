import color
import string_handling
import unittest

class TestStringHandling(unittest.TestCase):
  def test_ana(self):
    self.assertEqual(string_handling.ana("apple"), "an")
    self.assertEqual(string_handling.ana("egg"), "an")
    self.assertEqual(string_handling.ana("illness"), "an")
    self.assertEqual(string_handling.ana("oval"), "an")
    self.assertEqual(string_handling.ana("umpire"), "an")
    self.assertEqual(string_handling.ana("chain"), "a")
    self.assertEqual(string_handling.ana("dog"), "a")

  def test_oaus(self):
    self.assertTrue(string_handling.alpha_under_score("awef_as_htr_o"))
    self.assertFalse(string_handling.alpha_under_score("user@gmailDOTcom"))
    self.assertFalse(string_handling.alpha_under_score("userATgmail.com"))
    self.assertFalse(string_handling.alpha_under_score("Hello5world"))
    self.assertFalse(string_handling.alpha_under_score("Goodbye!"))

  def test_oanu(self):
    self.assertTrue(string_handling.alpha_num_under_score("janitors_closet12"))
    self.assertTrue(string_handling.alpha_num_under_score("hallway_path"))
    self.assertTrue(string_handling.alpha_num_under_score("hallway13"))
    self.assertFalse(string_handling.alpha_num_under_score("janitor.closet"))
    self.assertFalse(string_handling.alpha_num_under_score("hall@casino"))    

  def test_ans(self):
    self.assertTrue(string_handling.alpha_num_space("janitors closet12"))
    self.assertTrue(string_handling.alpha_num_space("hallway path"))
    self.assertTrue(string_handling.alpha_num_space("hallway13"))
    self.assertFalse(string_handling.alpha_num_space("janitor.closet"))
    self.assertFalse(string_handling.alpha_num_space("hall@casino"))

  def test_ordinal(self):
    self.assertEqual(string_handling.ordinal(0), "0th")
    self.assertEqual(string_handling.ordinal(41), "41st")
    self.assertEqual(string_handling.ordinal(102), "102nd")
    self.assertEqual(string_handling.ordinal(303), "303rd")
    self.assertEqual(string_handling.ordinal(5024), "5024th")
    self.assertEqual(string_handling.ordinal(3055), "3055th")
    self.assertEqual(string_handling.ordinal(10296), "10296th")
    self.assertEqual(string_handling.ordinal(12447), "12447th")
    self.assertEqual(string_handling.ordinal(399418), "399418th")
    self.assertEqual(string_handling.ordinal(102249), "102249th")

  def test_oxford_comma(self):
    self.assertEqual(string_handling.oxford_comma(['ball', 'toy']), "ball and toy")
    self.assertEqual(string_handling.oxford_comma(['dog', 'cat', 'mouse']), "dog, cat, and mouse")
    self.assertEqual(string_handling.oxford_comma(['penny', 'nickel', 'dime', 'quarter']), "penny, nickel, dime, and quarter")

  def test_valid_id(self):
    self.assertTrue(string_handling.valid_id("janitors_closet12"))
    self.assertTrue(string_handling.valid_id("hallway_path"))
    self.assertTrue(string_handling.valid_id("hallway13"))
    self.assertFalse(string_handling.valid_id("janitor.closet"))
    self.assertFalse(string_handling.valid_id("hall@casino"))

  def test_strip_tags(self):
    original1 = "<p>The quick <c1>brown<c0> fox jumped over the lazy dog.</p>"
    goal1 = "The quick brown fox jumped over the lazy dog."

    original2 = "<p> </p> <c1> <c2>  <c3>"
    goal2 = "     "

    self.assertEqual(string_handling.strip_tags(original1), goal1)
    self.assertEqual(string_handling.strip_tags(original2), goal2)

  def test_paragraph(self):

    indented_lines_width_7 = [
      "  ... .",         # two words with indent fit exactly
      "... ..",          # two words fit with spare space
      ". .. ..",         # three words fit exactly
      ".......",         # one word fits exactly
      "..........",      # one word too big
      ". . . .",         # four words fit exactly
    ]

    one_long_line = " ".join(indented_lines_width_7)
    paragraph = "\r\n".join(indented_lines_width_7)

    self.assertEqual(string_handling.paragraph(one_long_line, 7, indent=True), paragraph)

  def test_parse_reference(self):
    global_id = "some_zone_123"
    local_id = "some_thing_123"
    reference = f"{global_id}[{local_id}]"

    result_global, result_local = string_handling.parse_reference(reference)

    self.assertEqual(result_global, global_id)
    self.assertEqual(result_local, local_id)

    result_global, result_local = string_handling.parse_reference(local_id)

    self.assertIsNone(result_global)
    self.assertEqual(result_local, local_id)

  def test_proofread(self):
    pairs = (
      (
         "Hello , how are     you guys ?",
         "Hello, how are you guys?"
      ),
      (
         "This sentence , has three   periods   .  .  .",
         "This sentence, has three periods..."
      )
    )

    for pair in pairs:
      self.assertEqual(string_handling.proofread(pair[0]), pair[1])

  def test_yesno(self):
    self.assertEqual(string_handling.yesno(True), "yes")
    self.assertEqual(string_handling.yesno(False), "no")

    self.assertEqual(string_handling.yesno(1), "yes")
    self.assertEqual(string_handling.yesno(0), "no")

  def test_tidy_color_tags(self):
    pairs = (
      (
        "... <c3> ...",      # color code trapped between space
        "...  <c3>..."       # space moved to left
      ),
      (
        "... <c1>",          # string terminated with ' <cX>'
        "...<c1> "           # space moved to the right
      ),
      (
        ".. <c3><c1> ..",    # redundant color codes
        "..  <c1>.."         # useless one removed
      ),
      (
        ". <c4> <c5><c2>   <c3> .",
        ".      <c3>."
      )
    )

    for pair in pairs:
      self.assertEqual(string_handling.tidy_color_tags(pair[0]), pair[1])

  def test_proc_color(self):
    pre = "This sentence <c1>has<c3> color <c6>codes.<c0>"
    post = "This sentence {}has{} color {}codes.{}".format(
      color.ansi_color_sequence(1),
      color.ansi_color_sequence(3),
      color.ansi_color_sequence(6),
      color.ansi_color_sequence(0)
    )

    self.assertEqual(string_handling.proc_color(pre), post)

if __name__ == '__main__':
  #x = string_handling.proofread("This sentence , has three   periods   .  .  .")
  #print(string_handling.proofread(x))
  print("\nTODO: re-write the proofread function\n")
  unittest.main()
