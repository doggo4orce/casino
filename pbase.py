from color import *
import config
import file_handling
import logging
import os
import pc
import string_handling

# default values to be used when loading characters from save files
PF_DEFAULT_TITLE = config.DEFAULT_TITLE
PF_DEFAULT_ROOM = config.VOID_ROOM

ptable = list()

# much of this code is repeated in load_char_by_name, but repetition seems necessary
# to avoid loading the entire character just to look up a single field
def field_by_name(name, field):
  with open(f"{config.PFILES_PATH}{name.lower()}.plr") as rf:
    line_number = 0
    for line in rf:
      line_number += 1
      # allows us to ignore comments and blank lines
      if line == "\n" or line[0] == '#':
        continue
      var_list = line.split()
      tag = var_list[0]
      value = " ".join(var_list[1:])
      if tag[-1] != ":":
        logging.error(f"Line ({line_number}) -- Error: Expected ':' at the end of tag while loading {name}.plr")
        logging.error("See field_by_name.")
        return False
      tag = tag[0:len(tag) - 1] # remove the semi-colon after confirming it's there
      if tag == field:
        return value

def verify_password(name, password):
  return field_by_name(name, "password") == password

def num_players():
  return len(ptable)

def id_by_name(name):
  for p in ptable:
    if p["name"].lower() == name.lower():
      return p["id"]
  return None

def name_by_id(id):
  return ptable[id]["name"]

def check_file_structure():
  complaint = "'{}' does not exist.  Creating it."
  if not os.path.exists(config.LIB_FOLDER):
    logging.info(complaint.format(config.LIB_FOLDER))
    os.system("mkdir {}".format(config.LIB_FOLDER))
  if not os.path.exists(config.PFILES_PATH):
    logging.info(complaint.format(config.PFILES_PATH))
    os.system("mkdir {}".format(config.PFILES_PATH))
  if not os.path.exists(config.PLAYER_INDEX_PATH):
    logging.info(complaint.format(config.PLAYER_INDEX_PATH))
    os.system("touch {}".format(config.PLAYER_INDEX_PATH))

def load_ptable():
  logging.info("Generating player index.")
  with open(config.PLAYER_INDEX_PATH, "r") as rf:
    for line in rf:
      var_list = line.split()
      if len(var_list) != 2:
        logging.error(f"Error: '{config.PLAYER_INDEX_PATH}' is corrupted.  Aborting.")
        exit(1)
      add_player_to_index(var_list[1])
  logging.info(f"   {num_players()} players in database.")

def update_index_file():
  with open(config.PLAYER_INDEX_PATH, "w") as wf:
    for j in range(0, num_players()):
      p_element = ptable[j]
      wf.write(f"{p_element['id']} {p_element['name']}\r\n")

def add_player_to_index(name):
  ptable.append({"id": num_players() + 1, "name": name.lower()})

def load_char_by_name(name):
  result = pc.pc()
  result.room = PF_DEFAULT_ROOM
  result.title = PF_DEFAULT_TITLE
  line_number = 0

  if id_by_name(name) == None:
    # TODO: replace with index error exception
    logging.error(f"Error: Trying to load pfile for name {name} which is not contained in the index.")
    return
  else:
    result.id = id_by_name(name)

  rf = open(f"{config.PFILES_PATH}{name.lower()}.plr")
  file_handling.parse_generic(result, rf)
  return result

def ptable_str():
  ret_val = ""
  for p in ptable:
    ret_val += f"{p['id']} {p['name']}\n"

if __name__ == '__main__':
  print(field_by_name("bob", "titl"))
