from model import *
from sys import argv
from color_log import Log


def update_proxy(items: str):
  data = ProxyData()
  for item in items.split(','):
    data.add(item)
  Log.success(f'update {len(data)} proxy')
  data.save()


if __name__ == '__main__':
  try:
    update_proxy('\n' + argv[1])
    push_to_github(f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())} update item')
  except Exception as e:
    print(e)
    print('please input site')
