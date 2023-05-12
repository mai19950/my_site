from sys import argv
from add_proxy import *


def del_item(item: str):
  with open(join_dir('proxy.txt'), mode="r", encoding="utf8") as f:
    data = f.readlines()
  for it in data:
    if item in it:
      data.remove(it)
  with open(join_dir('proxy.txt'), mode="w+", encoding="utf8") as f:
    f.writelines(data)
  with open(join_dir('proxy.base64'), mode="wb+") as f:
    f.write(base64.b64encode(bytes('\n'.join(data), 'utf-8')))


if __name__ == '__main__':
  try:
    del_item(argv[1])
    push_to_github(f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} delete item')
  except:
    print('please input site')