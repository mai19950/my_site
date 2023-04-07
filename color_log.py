from typing import Any, Type, Callable, List, Tuple, Union, Literal
from functools import reduce
from colorama import init
init(autoreset=True)

Dicts = Union[dict, List[dict]]
PrimitiveType = Union[str, int, float]
LogJsonColor = Union[Literal["red_bg"], Literal["gray_bg"], Literal["black"], 
  Literal["red"], Literal["green"], Literal["yellow"], Literal["blue"], 
  Literal["fuchsia"], Literal["cyan"], Literal["white"]]

class BatchClassMethodMeta(type):
  def __new__(cls, name: str, bases: Tuple, dct: dict):
    # 获取要添加的类方法列表
    class_methods: List[Tuple[str, Callable]] = dct.get('_class_methods_', [])

    # 遍历列表，为类添加类方法
    for method_name, method_func, method_annotations in class_methods:
      # 创建 lambda 函数，将参数传递给原始函数，并添加类型注解
      method_lambda = cls.create_lambda(method_func, method_annotations)
      # 将 lambda 函数添加为类方法
      dct[method_name] = classmethod(method_lambda)

    # 创建新类
    new_cls = super().__new__(cls, name, bases, dct)
    return new_cls
  
  @staticmethod
  def create_lambda(method_func: Callable, method_annotations: dict) -> Callable:
    def method_lambda(cls: Type, *args: Any, **kwargs: Any) -> Any:
      annotated_args = [method_annotations.get(arg, arg) for arg in args]
      annotated_kwargs = {
        key: method_annotations.get(key, value) for key, value in kwargs.items()
      }
      return method_func(cls, *annotated_args, **annotated_kwargs)
    return method_lambda


class BaseClass(metaclass=BatchClassMethodMeta):
  _class_methods_: List[Tuple[str, Callable, dict]] = []

"""
格式：\033[显示方式;前景色;背景色m

说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色
显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见

例子：
\033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
\033[0m          <!--采用终端默认设置，即取消颜色设置-->

# -*- coding:utf-8 -*-
print("\033[1;30m 字体颜色：白色\033[0m")
print("\033[1;31m 字体颜色：红色\033[0m")
print("\033[1;32m 字体颜色：深黄色\033[0m")
print("\033[1;33m 字体颜色：浅黄色\033[0m")
print("\033[1;34m 字体颜色：蓝色\033[0m")
print("\033[1;35m 字体颜色：淡紫色\033[0m")
print("\033[1;36m 字体颜色：青色\033[0m")
print("\033[1;37m 字体颜色：灰色\033[0m")
print("\033[1;38m 字体颜色：浅灰色\033[0m")

print("背景颜色：白色   \033[1;40m    \033[0m")
print("背景颜色：红色   \033[1;41m    \033[0m")
print("背景颜色：深黄色 \033[1;42m    \033[0m")
print("背景颜色：浅黄色 \033[1;43m    \033[0m")
print("背景颜色：蓝色   \033[1;44m    \033[0m")
print("背景颜色：淡紫色 \033[1;45m    \033[0m")
print("背景颜色：青色   \033[1;46m    \033[0m")
print("背景颜色：灰色   \033[1;47m    \033[0m")
"""

__color_name_map__ = {
  "red_bg":     "37;41m",
  "gray_bg":    "36;47m",
  "black":      "30;40m", 
  "red":        "31;40m", 
  "green":      "32;40m", 
  "yellow":     "33;40m", 
  "blue":       "34;40m", 
  "fuchsia":    "35;40m", 
  "cyan":       "36;40m", 
  "white":      "37;40m", 
}



# class Text(BaseClass):
#   # @classmethod
#   # def _set_color(cls, text: str, color_num: str) -> str:
#   #   return "\033[1;{}{}\033[0m".format(color_num, text)

#   _class_methods_ = [
#     (
#       name, 
#       lambda cls, text, color=color: "\033[1;{}{}\033[0m".format(color, text),
#       {"text": str}
#     ) for name, color in __color_name_map__.items()
#   ]

class Text:
  @classmethod
  def _set_color(cls, text: PrimitiveType, color_num: str, *args, **kwargs) -> str:
    return "\033[1;{}{}\033[0m".format(color_num, text)

  @classmethod
  def red_bg(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "37;41m", *args, **kwargs)

  @classmethod
  def gray_bg(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "36;47m", *args, **kwargs)

  @classmethod
  def black(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "30;40m", *args, **kwargs)

  @classmethod
  def red(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "31;40m", *args, **kwargs)

  @classmethod
  def green(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "32;40m", *args, **kwargs)

  @classmethod
  def yellow(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "33;40m", *args, **kwargs)

  @classmethod
  def blue(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "34;40m", *args, **kwargs)

  @classmethod
  def fuchsia(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "35;40m", *args, **kwargs)

  @classmethod
  def cyan(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "36;40m", *args, **kwargs)

  @classmethod
  def white(cls, text: PrimitiveType, *args, **kwargs) -> str:
    return cls._set_color(text, "37;40m", *args, **kwargs)

  @classmethod
  def list_text(cls, data: list, indent: int = 1, tab: str= ' ') -> str:
    indent *= 2
    output = "[\n"
    for it in data:
      output += f"{tab * indent}{it},\n"
    output += f"{tab* (indent - 2)}]"
    return output
  
  @classmethod
  def json_text(cls, data: Dicts, indent: int = 1, tab: str= ' ') -> str:
    if isinstance(data, list):
      return cls.list_text(data, indent, tab)
    indent *= 2
    output = "{\n"
    for k, v in data.items():
      output += f"{tab * indent}{k}: {cls.list_text(v, indent=2) if isinstance(v, list) else v},\n"
    output += f"{tab * (indent - 2)}}}"
    return output

class Log(Text):

  @staticmethod
  def join_str(*args):
    return reduce(lambda x,y: f"{x} {y}", args, "").strip()

  @classmethod
  def set_pad(cls, *args, **kwargs) -> tuple:
    content = ""
    pad_left = pad_right = 0
    if 'pad_left' in kwargs:
      pad_left = kwargs['pad_left']
      del kwargs['pad_left']
    if 'pad_right' in kwargs:
      pad_right = kwargs['pad_right']
      del kwargs['pad_right']

    if pad_left != 0 and pad_right == 0:
      content = cls.join_str(*args).rjust(pad_left, ' ')
    elif pad_left == 0 and pad_right != 0:
      content = cls.join_str(*args).ljust(pad_right, ' ')
    else:
      content = cls.join_str(*args)
    return (content, kwargs)

  @classmethod
  def color_print(cls, color_fn: Callable, *args, **kwargs):
    content, kw = cls.set_pad(*args, **kwargs)
    return print(color_fn(text=content), **kw)
    # return print("\033[1;{}{}\033[0m".format(color_num, content), **kwargs)

  @classmethod
  def red_bg(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).red_bg, *args, **kwargs)

  @classmethod
  def gray_bg(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).gray_bg, *args, **kwargs)

  @classmethod
  def black(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).black, *args, **kwargs)

  @classmethod
  def red(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).red, *args, **kwargs)

  @classmethod
  def green(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).green, *args, **kwargs)

  @classmethod
  def yellow(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).yellow, *args, **kwargs)

  @classmethod
  def blue(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).blue, *args, **kwargs)

  @classmethod
  def fuchsia(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).fuchsia, *args, **kwargs)

  @classmethod
  def cyan(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).cyan, *args, **kwargs)

  @classmethod
  def white(cls, *args, **kwargs):
    return cls.color_print(super(Log, cls).white, *args, **kwargs)

  @classmethod
  def error(cls, *args, **kwargs):
    cls.red_bg("[error]:", *args, **kwargs)

  @classmethod
  def info(cls, *args, **kwargs):
    cls.cyan("[info]:", *args, **kwargs)

  @classmethod
  def success(cls, *args, **kwargs):
    cls.green("[success]:", *args, **kwargs)

  @classmethod
  def warn(cls, *args, **kwargs):
    cls.yellow("[warn]:", *args, **kwargs)

  @classmethod
  def json(cls, data: Dicts, color: LogJsonColor = "white"):
    # cls[color](super().json_text(data))
    getattr(cls, color)(super().json_text(data))


class Info(Log):
  @classmethod
  def error(cls, *args, **kwargs):
    content, kw = super().set_pad(f"[{super(Log, cls).red('error')}]: ", *args, **kwargs)
    print(content, **kw)

  @classmethod
  def info(cls, *args, **kwargs):
    content, kw = super().set_pad(f"[{super(Log, cls).cyan('info')}]: ", *args, **kwargs)
    print(content, **kw)

  @classmethod
  def success(cls, *args, **kwargs):
    content, kw = super().set_pad(f"[{super(Log, cls).green('success')}]: ", *args, **kwargs)
    print(content, **kw)

  @classmethod
  def warn(cls, *args, **kwargs):
    content, kw = super().set_pad(f"[{super(Log, cls).yellow('warn')}]: ", *args, **kwargs)
    print(content, **kw)

  @classmethod
  def json(cls, data: Dicts):
    cls.info(super().json(data))


if __name__ == '__main__':
  print('\033[1;31;40m')
  print('*' * 50)
  print('*HOST:\t', 2002)
  print('*URI:\t', 'http://127.0.0.1')
  print('*ARGS:\t', 111)
  print('*TIME:\t', '22:28')
  print('*' * 50)
  print('\033[0m')
  print('\033[1;31;40m ', "test", ' \033[0m')
  print("Text class Example: ", Text.red("text red"))
  Log.red('red')
  Log.green('green')
  Log.yellow('yellow')
  Log.blue('blue')
  Log.fuchsia('fuchsia')
  Log.cyan('cyan')
  Log.black('black')
  Log.white('white')
  Log.success('success')
  Log.error('error')
  Log.info('info')
  Log.warn('warn')
  Info.success('info success')
  Info.error('info error')
  Info.info('info info')
  Info.warn('info warn')
  l = Log()
  # print(Log.__dict__)


