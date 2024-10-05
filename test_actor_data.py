import actor_data
import behaviour_data
import cmd_trig_data
import hbeat_proc_data

import unittest

class TestActorData(unittest.TestCase):
  def test_actor(self):

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

    ad = actor_data.actor_data()

    ad.assign_procs(
      [ pct1, pct2, sct1, sct2, hb1, hb2 ]
    )

    msg = ad.call_prefix_cmd_trigs("grottomud","beltriz", "slap", "in the face", "wld_files")
    if msg == cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER:
      print("\n\nInterpreter blocked!\n\n")
    

    ad.call_suffix_cmd_trigs("grottomud","roobiki", "cry", "into his arms", "social_files")
    ad.call_hbeat_procs("uossmud", "sql")

    ad.remove_procs()

    print("Since procs were removed, no new output should be below this line.")

    ad.call_hbeat_procs("uossmud", "sql")

if __name__ == "__main__":
  unittest.main()