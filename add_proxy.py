import base64 , os
from sys import argv
import time


def update_proxy(item: str):
  with open('./proxy.txt', mode="r", encoding="utf8") as f:
    data = f.readlines()
  data.append(item)
  with open('./proxy.txt', mode="w+", encoding="utf8") as f:
    f.writelines(data)
  with open('proxy.base64', mode="wb+") as f:
    f.write(base64.b64encode(bytes('\n'.join(data), 'utf-8')))


def push_to_github():
  os.system('git add . ')
  os.system(f'git commit -m "{time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())} update item"')
  os.system("git push")


if __name__ == '__main__':
  try:
    update_proxy('\n' + argv[1])
    push_to_github()
  except:
    print('please input site')
