import base64
from add_proxy import push_to_github

def convert_to_base64():
  proxy_list = open('proxy.txt', mode="r", encoding="utf8")
  with open('proxy.base64', mode="wb+") as f:
    f.write(base64.b64encode(bytes(proxy_list.read(), 'utf-8')))
    proxy_list.close()


if __name__ == '__main__':
  convert_to_base64()
  push_to_github()