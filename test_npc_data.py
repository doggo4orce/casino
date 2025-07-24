import behaviour_data
import cmd_trig_data
import character_data
import hbeat_proc_data
import npc_data
import npc_proto_data
import unique_id_data

import unittest

class TestNpcData(unittest.TestCase):
  def test_npc_data(self):
    npc = npc_data.npc_data()
    npc.zone_id = "wild_zone"
    npc.id = "wild_dog"
    npc.name = "wild dog"
    npc.desc = "It looks wild and ravenous."
    npc.ldesc = "A wild dog runs around here and barks."
    npc.room = unique_id_data.unique_id_data("stockville", "casino")
    npc.reset_aliases("wild", "dog")
    # print(npc.debug())

    self.assertEqual(npc.zone_id, "wild_zone")
    self.assertEqual(npc.id, "wild_dog")
    self.assertEqual(npc.name, "wild dog")
    self.assertEqual(npc.desc, "It looks wild and ravenous.")
    self.assertEqual(npc.ldesc, "A wild dog runs around here and barks.")

  def test_from_proto(self):
    npc_p = npc_proto_data.npc_proto_data()
    npc_p.id = 'happy_npc'
    npc_p.zone_id = 'test_zone'
    npc_p.name = "a happy npc"
    npc_p.remove_all_aliases()
    npc_p.add_alias("happy")
    npc_p.add_alias("npc")
    npc_p.ldesc = "a happy npc wanders here"
    npc_p.desc = "it looks happy"
    
    npc = npc_data.npc_data(npc_p)
    print(npc.debug())

  def test_from_char(self):
    ch = character_data.character_data()
    ch.name = "bob"
    ch.desc = "<p>This is Bob.</p>"
    ch.ldesc = "Bob is standing around."
    ch.room = unique_id_data.unique_id_data("stockville", "casino")
    ch.reset_aliases("bob", "nice")

    npc = npc_data.npc_data.from_character(ch)

    # print(ch.debug() + "\r\n")
    # print(npc.debug() + "\r\n")

  def test_copy_from(self):
    npc = npc_data.npc_data()
    npc.zone_id = "wild_zone"
    npc.id = "wild_cat"
    npc.name = "wild cat"
    npc.desc = "It looks wild and cat-like."
    npc.ldesc = "A wild cat runs around here and meows."
    npc.room = unique_id_data.unique_id_data("stockville", "casino")
    npc.reset_aliases("wild", "cat")

    def prefix_func1(mud, me, ch, command, argument, db):
      out_str = f"prefix_func1:\n"
      out_str += f"mud: {mud}\n"
      out_str += f"me: {me}\n"
      out_str += f"ch: {ch}\n"
      out_str += f"command: {command}\n"
      out_str += f"argument: {argument}\n"
      out_str += f"db: {command}"
      print(out_str)
      return cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER
    def prefix_func2(mud, me, ch, command, argument, db):
      out_str = f"prefix_func2:\n"
      out_str += f"mud: {mud}\n"
      out_str += f"me: {me}\n"
      out_str += f"ch: {ch}\n"
      out_str += f"command: {command}\n"
      out_str += f"argument: {argument}\n"
      out_str += f"db: {command}"
      print(out_str)
    def suffix_func1(mud, me, ch, command, argument, db):
      out_str = f"suffix_func1:\n"
      out_str += f"mud: {mud}\n"
      out_str += f"me: {me}\n"
      out_str += f"ch: {ch}\n"
      out_str += f"command: {command}\n"
      out_str += f"argument: {argument}\n"
      out_str += f"db: {command}"
      print(out_str)
    def suffix_func2(mud, me, ch, command, argument, db):
      out_str = f"suffix_func_2:\n"
      out_str += f"mud: {mud}\n"
      out_str += f"me: {me}\n"
      out_str += f"ch: {ch}\n"
      out_str += f"command: {command}\n"
      out_str += f"argument: {argument}\n"
      out_str += f"db: {command}"
      print(out_str)
    def hbeat_proc1(mud, me, db):
      out_str = f"hbeat_proc1:\n"
      out_str += f"mud: {mud}\n"
      out_str += f"me: {me}\n"
      out_str += f"db: {db}"
      print(out_str)
    def hbeat_proc2(mud, me, db):
      out_str = f"hbeat_proc2:\n"
      out_str += f"mud: {mud}\n"
      out_str += f"me: {me}\n"
      out_str += f"db: {db}"

    pct1 = cmd_trig_data.prefix_cmd_trig_data("prefix 1", prefix_func1)
    pct2 = cmd_trig_data.prefix_cmd_trig_data("prefix 2", prefix_func2)
    sct1 = cmd_trig_data.suffix_cmd_trig_data("suffix 1", suffix_func1)
    sct2 = cmd_trig_data.suffix_cmd_trig_data("suffix 2", suffix_func2)
    hb1 = hbeat_proc_data.hbeat_proc_data("heartbeat 1", hbeat_proc1)
    hb2 = hbeat_proc_data.hbeat_proc_data("heartbeat 2", hbeat_proc2)

    npc.assign_procs(
      [ pct1, pct2, sct1, sct2, hb1, hb2 ]
    )

    new_npc = npc_data.npc_data()
    new_npc.copy_from(npc)

    print(new_npc.debug())
if __name__ == "__main__":
  unittest.main()