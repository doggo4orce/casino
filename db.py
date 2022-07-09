import collections
import structs
import logging
import room

npc_proto_data = collections.namedtuple(
  'mob_proto_data', [
    'entity',
    'command_triggers',
    'heart_beat_procs'
    # put stuff below like stats, gold, hp, etc.
  ]
)

obj_proto_data = collections.namedtuple(
  'obj_proto_data', [
    'entity'
    # put stuff below like type (weapon, lantern), price, weight etc.
  ]
)

def parse_tag(line):
  var_list = line.split()
  return var_list[0], " ".join(var_list[1:])

def parse_npc(rf):
  ret_val_ent = structs.entity()
  while True:
    line = rf.readline()
    if line == "S\n":
      break
    # expecting a tag for sure
    tag, value = parse_tag(line)
    # if we don't get a tag this file is not formatted properly
    if tag[-1] != ":":
      logging.error(f"Error: Expected ':' at the end of tag {tag} while loading")
      return
    # remove the colon and convert to lowercase
    tag = tag[0:len(tag) - 1].lower()
    # ready to interpret the actual tag
    if tag == "name":
      ret_val_ent.name = value
    elif tag == "namelist":
      ret_val_ent.namelist = value.split(" ")
    elif tag == "desc":
      ret_val_ent.desc = value
    elif tag == "ldesc":
      ret_val_ent.ldesc = value
    else:
      logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")
  # all the data is loaded, now we can store it to the proto
  return npc_proto_data(ret_val_ent, list(), list())

def parse_obj(rf):
  ret_val_ent = structs.entity()
  while True:
    line = rf.readline()
    if line == "S\n":
      break
    # expecting a tag for sure
    tag, value = parse_tag(line)
    # if we don't get a tag this file is not formatted properly
    if tag[-1] != ":":
      logging.error(f"Error: Expected ':' at the end of tag {tag} while parsing {rf.name}.")
      return
    # remove the colon and convert to lowercase
    tag = tag[0:len(tag) - 1].lower()
    # ready to interpret the actual tag
    if tag == "name":
      ret_val_ent.name = value
    elif tag == "namelist":
      ret_val_ent.namelist = value.split(" ")
    elif tag == "ldesc":
      ret_val_ent.ldesc = value
    elif tag == "desc":
      ret_val_ent.desc = value
    else:
      logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")
  # all the data is loaded, now we can store it to the proto
  return obj_proto_data(ret_val_ent)

def parse_room(rf):
  dir_tags = [dir.name for dir in room.direction]
  ret_val = room.room()
  while True:
    line = rf.readline()
    if line == "S\n":
      break
    # expecting a tag for sure
    tag, value = parse_tag(line)
    # if we don't get a tag this file is not formatted properly
    if tag[-1] != ":":
      logging.error(f"Error: Expected ':' at the end of tag {tag} while parsing {rf.name}.")
      return
    # remove the colon and convert to lowercase
    tag = tag[0:len(tag) - 1].lower()
    # ready to interpret the actual tag
    if tag == "name":
      ret_val.name = value
    elif tag == "desc":
      ret_val.desc = value
    elif tag.upper() in dir_tags:
      # found an exit
      ret_val.connect(room.direction(room.direction[tag.upper()]), int(value))
    else:
      logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")
  return ret_val