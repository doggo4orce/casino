import db_column
import mudlog

class db_result_set:
  def __init__(self, *column_names):
    self._column_names = list()
    self._results = list()

    for column_name in column_names:
      self.add_column(column_name)

  """Additional Properties:

     columns     <- returns list of column names
     results     <- returns list of results
     num_results <- counts results"""

  @property
  def columns(self):
    return [name for name in self._column_names]

  @property
  def results(self):
    return [result for result in self._column_results]

  @property
  def num_results(self):
    return len(self._results)

  """add_column(name)      <- insert new column, pads result fields with None
     delete_column(name)   <- removes column and corresponding field from results
     add_result(result)    <- insert new result to self._results
     delete_result(result) <- remove result from self._results"""

  def add_column(self, name):
    if db_column.valid_column_name(name):
      self._column_names.append(name)
    for result in self._results:
      result[name] = None

  def delete_column(self, name):
    if name in self.columns:
      self._column_names.remove(name)

    for result in self._results:
      if name in result:
        result.delete_field(name)

  def add_result(self, result):
    if result.fields != self._column_names:
      mudlog.error(f"Trying to add result\r\n{result}\r\nto result set with incompatible fields")
    else:
      self._results.append(result)

  def delete_result(self, result):
    self._results.remove(result)

  def __iter__(self):
    return db_result_set_iterator(self._results)

  def __contains__(self, result):
    return result in self._results

  def __getitem__(self, key):
    return self._results[key]

  def __str__(self):
    ret_val = ""
    for result in self._results:
      ret_val += str(result) + '\r\n'
    if self.num_results > 0:
      ret_val = ret_val[:-2]
    return ret_val

class db_result_set_iterator:
  def __init__(self, new_result_set):
    self._result_set = new_result_set
    self._index = 0

  def __next__(self):
    if self._index < len(self._result_set):
      ret_val = self._result_set[self._index]
      self._index += 1
      return ret_val
    else:
      raise StopIteration
