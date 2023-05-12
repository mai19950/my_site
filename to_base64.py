from add_proxy import *

def convert_to_base64():
  proxy_list = open(join_dir('proxy.txt'), mode="r", encoding="utf8")
  with open(join_dir('proxy.base64'), mode="wb+") as f:
    f.write(base64.b64encode(bytes(proxy_list.read(), 'utf-8')))
    proxy_list.close()


if __name__ == '__main__':
  convert_to_base64()
  push_to_github(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) +'update base64')