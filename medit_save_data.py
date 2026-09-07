import dataclasses
import text_data
import unique_id_data

@dataclasses.dataclass
class medit_save_data:
  """ fill this in when medit is developed """
  def __init__(self):
    self.uid = unique_id_data.unique_id_data()
    self.name = "An unfinished NPC"
    self.desc = text_data.text_data("<p>It looks unfinished.</p>")
    self.ldesc = "An unfinished NPC stands here."
    self.aliases = ["unfinished", "npc"]