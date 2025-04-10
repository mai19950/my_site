
import os
import time
import base64
from color_log import *
from clash_handler.main import *

SUB_DIR = "sub"
PROXY_FILE = f"{SUB_DIR}/proxy.txt"
BASE64_FILE = f"{SUB_DIR}/proxy.base64"
YAML_FILE = f"{SUB_DIR}/proxy.yaml"

PC_IP = "192.168.0.110"
IPAD_IP = "192.168.0.112"

LOCAL_PROXY = [
  f"socks5://{PC_IP}:1081#LOCAL",
  f"socks://{PC_IP}:1081#LOCAL",
  # f"socks://Og==@{PC_IP}:1081#LOCAL",
  f"socks://{IPAD_IP}:9988#LOCAL_IPAD",
  f"socks5://{IPAD_IP}:9988#LOCAL_IPAD",
  # f"socks://Og=={IPAD_IP}:9988#LOCAL_IPAD",
  f"http://{PC_IP}:1082#LOCAL"
]

def join_dir(*paths):
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), *paths)


def deduplication(array: list) -> list:
  res = []
  for it in array:
    it = it.strip()
    if it == "" or (it in res):
      continue
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
    self.yaml_path = join_dir(YAML_FILE)
    self.__LOCAL_PROXY__ = LOCAL_PROXY
    self.__PROXY_DATA__ = []
    
    self.update_data_from_file()

  @property
  def data(self) -> list:
    return self.__PROXY_DATA__

  @property
  def length(self) -> int:
    return len(self.__PROXY_DATA__)

  @classmethod
  def filter_real_data(cls, data: list) -> list:
    res = [it.strip() for it in data]
    return list(filter(lambda x: ("#LOCAL" not in x), res))

  def index(self, idx: int) -> str:
    return self.__PROXY_DATA__[idx]

  def update_data_from_file(self):
    with open(self.proxy_path, mode="r", encoding="utf8") as f:
      self.__PROXY_DATA__ = self.filter_real_data(f.readlines())
      return self

  def add(self, item: str):
    self.__PROXY_DATA__ = deduplication(self.__PROXY_DATA__ + [item])
    return self

  def clear(self):
    self.__PROXY_DATA__ = []
    return self

  def remove(self, item: str):
    for it in self.__PROXY_DATA__:
      if item in it:
        self.__PROXY_DATA__.remove(it)    
        return self

  def update(self, data: list):
    self.__PROXY_DATA__ = data
    return self

  def show(self):
    Log.cyan('\n'.join(self.__PROXY_DATA__))
    return self

  def to_yaml(self, data: list):
    nodes = CollectNodes().parse(data)
    nodes = ClashConfig.to_yaml(nodes.nodes, indent=2)
    # print(nodes)
    with open(self.yaml_path, mode="w+", encoding="utf8") as f:
      f.write("proxies:\n" + nodes)

  def save(self, msg: str = str(time.localtime())):
    # Log.json(self.__PROXY_DATA__, 'cyan')
    save_data = self.__LOCAL_PROXY__ + self.__PROXY_DATA__
    self.to_yaml(save_data)
    self.show()
    with open(self.proxy_path, mode="w+", encoding="utf8") as f:
      f.write('\n'.join(save_data))
    with open(self.base64_path, mode="wb+") as f:
      f.write(base64.b64encode(bytes('\n'.join(save_data), 'utf-8')))
    push_to_github(msg)


if __name__ == '__main__':
  ProxyData().show()
