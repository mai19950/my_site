import copy
from sys import argv
from model import *

class RemoveModel:
  def __init__(self) -> None:
    self.DataModel = ProxyData()
    self.bak_data = copy.deepcopy(self.DataModel.data)
    self.git_msg = f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} delete item'


  def del_items(self, items: list):
    for item in items:
      self.DataModel.remove(item)
    self.DataModel.save(self.git_msg)

  def del_item_from_index(self, index_list: list):
    for index in index_list:
      if index == "all":
        self.DataModel.clear().save(self.git_msg)
        exit(Text.red_bg("clear all data"))
      try:
        self.DataModel.remove(self.bak_data[int(index)])
      except Exception as e:
        Log.error(e.args)
        self.del_items(index_list)
        return 
    self.DataModel.save(self.git_msg)


if __name__ == '__main__':
  try:
    # del_item(argv[1])
    RemoveModel().del_item_from_index(argv[1].split(','))
    # push_to_github(f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} delete item')
  except:
    Log.error('please input site')