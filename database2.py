class row:
  def __init__(self, name):
    self._entries = dict()

class table:
   def __init__(self, name):
     self._columns = dict()
     self._rows = list()

   def add_column(self, name, type):
     self._columns[name]=type

   def delete_column(self, name):
     del self._columns[name]

   def num_columns(self):
     return len(self._columns.values())

   
rm_table = table('rm_table')

rm_table.add_column('zone_id', str)
rm_table.add_column('id', str)
rm_table.add_column('name', str)
rm_table.add_column('desc', str)

print(rm_table.num_columns())