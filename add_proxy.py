import base64 , os
from sys import argv
import time
from color_log import Log


def join_dir(*paths):
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), *paths)


def deduplication(array: list) -> list:
  res = []
  for it in array:
    it = it.strip()
    if it not in res:
      res.append(it)
  return res


def update_proxy(item: str):
  with open(join_dir("proxy.txt"), mode="r", encoding="utf8") as f:
    data = f.readlines()
  data.append(item)
  data = deduplication(data)
  Log.success(f'update {len(data)} proxy')
  with open(join_dir('proxy.txt'), mode="w+", encoding="utf8") as f:
    f.write('\n'.join(data))
  with open(join_dir('proxy.base64'), mode="wb+") as f:
    f.write(base64.b64encode(bytes('\n'.join(data), 'utf-8')))


def push_to_github(msg: str):
  os.chdir(join_dir())
  os.system('git add . ')
  os.system(f'git commit -m "{msg}"')
  os.system("git push")


if __name__ == '__main__':
  try:
    update_proxy('\n' + argv[1])
    push_to_github(f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} update item')
  except Exception as e:
    print(e)
    print('please input site')
