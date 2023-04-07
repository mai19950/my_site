from model import *

def convert_to_base64():
  ProxyData().save(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) +' update base64')


if __name__ == '__main__':
  convert_to_base64()
  # push_to_github(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) +'update base64')