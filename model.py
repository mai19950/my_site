
import os
import base64
import time

PROXY_FILE = "proxy.txt"
BASE64_FILE = 'proxy.base64'

def join_dir(*paths):
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), *paths)


def deduplication(array: list) -> list:
  res = []
  for it in array:
    it = it.strip()
    if it not in res:
      res.append(it)
  return res


def push_to_github(msg: str):
  os.chdir(join_dir())
  os.system('git add . ')
  os.system(f'git commit -m "{msg}"')
  os.system("git push")


class ProxyData:
  def __init__(self) -> None:
    self.proxy_path = join_dir(PROXY_FILE)
    self.base64_path = join_dir(BASE64_FILE)
    self.__PROXY_DATA__ = []
    
    self.update_data_from_file()

  @property
  def data(self) -> list:
    return self.__PROXY_DATA__

  @property
  def length(self) -> int:
    return len(self.__PROXY_DATA__)

  def index(self, idx: int) -> str:
    return self.__PROXY_DATA__[idx]

  def update_data_from_file(self):
    with open(self.proxy_path, mode="r", encoding="utf8") as f:
      self.__PROXY_DATA__ = f.readlines()
      return self

  def add(self, item: str):
    self.__PROXY_DATA__ = deduplication(self.__PROXY_DATA__ + [item])
    return self

  def remove(self, item: str):
    for it in self.__PROXY_DATA__:
      if item in it:
        self.__PROXY_DATA__.remove(it)    
        return self

  def update(self, data: list):
    self.__PROXY_DATA__ = data
    return self

  def save(self):
    with open(self.proxy_path, mode="w+", encoding="utf8") as f:
      f.write('\n'.join(self.__PROXY_DATA__))
    with open(self.base64_path, mode="wb+") as f:
      f.write(base64.b64encode(bytes('\n'.join(self.__PROXY_DATA__), 'utf-8')))
