import copy
import re
import yaml
import textwrap

template_path = "sub/customs/templates.yaml"
sub_dir = "sub/clash"
default_data = {
  "key": None,
  "<<": "*a1",
  "interval": 86400,
  "url": None
}

def parse_remarks(node: str) -> str:
  match = re.search(r'["\']?name["\']?:\s*([^,}]+)', node)
  return match.group(1).strip() if match else ''


def path_value(key: str, dirname: str = "proxy_providers") -> str:
  return f"./{dirname}/{key}.yaml"


def add_subscript_link(data: list, filename: str):
  providers = {}
  subscriptions = []
  data_copy = copy.deepcopy(data)
  for it in data_copy:
    try:
      key = it.pop('key')
    except Exception as e:
      print(e.args)
      continue
    if not key or key in providers:
      print("input unique key")
      continue
    providers[key] = it
    subscriptions.append(key)
  if not providers: return
  # providers = ["proxy-providers:\n"] + providers
  providers_yaml_str = "proxy-providers:\n" + textwrap.indent(
    yaml.dump(providers).replace("'", ""), "  ")

  with open(template_path, mode="r", encoding="utf-8") as f:
    lines = f.readlines()
  updated_lines = []
  for line in lines:
    if line.strip().startswith('subscriptions:'):
      updated_lines.append('subscriptions: &s1 {{use: [{0}]}}\n'.format(', '.join(subscriptions)))
    elif line.strip().startswith('proxy-providers:'):
      updated_lines.append(providers_yaml_str)
    else:
      updated_lines.append(line)
  with open(f"{sub_dir}/{filename}", mode="w+", encoding="utf-8") as f:
    f.writelines(updated_lines)


def update_rules():
  free_data = {
    **default_data,
    "key": "free",
    "interval": 300,
    "url": f"https://raw.githubusercontent.com/mai19950/sites/refs/heads/main/clash/free",
    "path": path_value("free")
  }
  git_data = {
    **default_data,
    "key": "git",
    "url": f"https://raw.githubusercontent.com/mai19950/my_site/main/sub/proxy.yaml",
    "path": path_value("git")
  }
  sos_data = {
    **default_data,
    "key": "sos",
    "url": f"https://SOS.CMLiussss.net/auto",
    "path": path_value("sos")
  }
  ripaojiedian_data = {
    **default_data,
    "key": "ripaojiedian",
    "interval": 43200,
    "url": f"https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/clash",
    "path": path_value("ripaojiedian")
  }
  nice_data = {
    "key": "nice",
    "type": "file",
    "path": path_value("nice"),
    "format": "yaml"
  }

  free_list = [ "abshare", "abshare3", "mkshare3", "mksshare", "tolinkshare2", "toshare5" ]
  for it in free_list:
    add_subscript_link([{
      **default_data,
      "key": it,
      "interval": 300,
      "url": f"https://raw.githubusercontent.com/mai19950/sites/refs/heads/main/clash/{it}.yaml",
      "path": path_value(it)
    }], f'{it}.yaml')

  add_subscript_link([free_data, sos_data, ripaojiedian_data], "all.yaml")

  add_subscript_link([free_data], "free.yaml")
  add_subscript_link([sos_data], "sos.yaml")
  add_subscript_link([ripaojiedian_data], "ripaojiedian.yaml")
  add_subscript_link([git_data], "git.yaml")
  add_subscript_link([nice_data], "nice.yaml")


def add_nodes_to_clash(nodes: str, filepath: str):
  node_list = []
  remarks = []
  for node in nodes.split('\n'):
    if node.strip() == "":
      continue
    node_list.append(f"{node}\n")
    remarks.append(parse_remarks(node))

  with open(template_path, mode="r", encoding="utf-8") as f:
    lines = f.readlines()
  updated_lines = []
  for line in lines:
    if line.strip().startswith('subscriptions:'):
      updated_lines.append('local_proxies: &s1 {{proxies: [{0}]}}\n'.format(', '.join(remarks)))
    elif line.strip().startswith('proxies:'):
      updated_lines = updated_lines + ["proxies:\n"] + node_list
    else:
      updated_lines.append(line)
  with open(filepath, mode="w+", encoding="utf-8") as f:
    f.writelines(updated_lines)

if __name__ == '__main__':
  update_rules()

