from model import *
from sys import argv

def update_proxy(items: str):
  data = ProxyData()
  for item in items.split(','):
    data.add(item)
  Log.success(f'update {data.length} proxy')
  data.save(f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} update item')


if __name__ == '__main__':
  try:
    update_proxy('\n' + argv[1])
    # push_to_github(f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} update item')
  except Exception as e:
    print(e)
    print('please input site')
