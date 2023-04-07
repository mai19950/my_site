import base64
from sys import argv
from add_proxy import push_to_github


def del_item(item: str):
  with open('./proxy.txt', mode="r", encoding="utf8") as f:
    data = f.readlines()
  for it in data:
    if item in it:
      data.remove(it)
  with open('./proxy.txt', mode="w+", encoding="utf8") as f:
    f.writelines(data)
  with open('proxy.base64', mode="wb+") as f:
    f.write(base64.b64encode(bytes('\n'.join(data), 'utf-8')))


if __name__ == '__main__':
  try:
    del_item(argv[1])
    push_to_github()
  except:
    print('please input site')