import copy
from sys import argv
from model import *

class RemoveModel:
  def __init__(self) -> None:
    self.DataModel = ProxyData()
    self.bak_data = copy.deepcopy(self.DataModel.data)


  def del_items(self, items: list):
    for item in items:
      self.bak_data.remove(item)
    self.DataModel.save()

  def del_item_from_index(self, index_list: list):
    for index in index_list:
      try:
        self.DataModel.remove(self.bak_data[int(index)])
      except Exception as e:
        Log.error(e.args)
        self.del_items(index_list)
        break
    self.DataModel.save()


if __name__ == '__main__':
  try:
    # del_item(argv[1])
    RemoveModel().del_item_from_index(argv[1].split(','))
    push_to_github(f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} delete item')
  except:
    print('please input site')