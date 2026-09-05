import buffer_data
import enum

class redit_state(enum.IntEnum):
  MEDIT_MAIN_MENU      = 1

def medit_display_main_menu(d):
  medit_save = d.olc.save_data
  desc_buffer = buffer_data.buffer_data(medit_save.desc.text)

  out_str = f"-- NPC ID : [{CYAN}{medit_save.uid.id}{NORMAL}]"
  out_str += f"        Zone ID : [{CYAN}{medit_save.uid.zone_id}{NORMAL}]\r\n"
  out_str += f"{GREEN}1{NORMAL}) NPC Name    : {YELLOW}{medit_save.name}{NORMAL}\r\n"
  out_str += f"{GREEN}2{NORMAL}) Description :\r\n"
  out_str += f"{desc_buffer.clean_up().display(d.character.page_width, indent=True, color=True)}{NORMAL}\r\n"
  out_str += f"{GREEN}3{NORMAL}) L-Desc      : {YELLOW}{medit_save.ldesc}{NORMAL}\r\n"
  out_str += f"{GREEN}C{NORMAL}) Copy NPC\r\n"
  out_str += f"{GREEN}Q{NORMAL}) Quit\r\n"
  d.write(out_str)