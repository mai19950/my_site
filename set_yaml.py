import re

template_path = "sub/customs/templates.yaml"
sub_dir = "sub/clash"

def parse_remarks(node: str) -> str:
  match = re.search(r'["\']?name["\']?:\s*([^,}]+)', node)
  return match.group(1).strip() if match else ''

def add_subscript_link(data: list, filename: str):
  providers = []
  subscriptions = []
  for it in data:
    providers += [
        f"  {it['key']}:\n",
        f"    <<: *a1\n",
        f"    interval: {it['interval']}\n",
        f"    url: {it['url']}\n",
        f"    path: ./proxy_providers/{it['key']}.yaml\n"
    ]
    subscriptions.append(it["key"])
  if not providers: return
  providers = ["proxy-providers:\n"] + providers

  with open(template_path, mode="r", encoding="utf-8") as f:
    lines = f.readlines()
  updated_lines = []
  for line in lines:
    if line.strip().startswith('subscriptions:'):
      updated_lines.append('subscriptions: &s1 {{use: [{0}]}}\n'.format(', '.join(subscriptions)))
    elif line.strip().startswith('proxy-providers:'):
      updated_lines += providers
    else:
      updated_lines.append(line)
  with open(f"{sub_dir}/{filename}", mode="w+", encoding="utf-8") as f:
    f.writelines(updated_lines)


def update_rules():
  free_data = {
      "key": "free",
      "interval": 900,
      "url": f"https://raw.githubusercontent.com/mai19950/free_nodes/refs/heads/main/sub/clash/free"
  }
  git_data = {
      "key": "git",
      "interval": 86400,
      "url": f"https://raw.githubusercontent.com/mai19950/my_site/main/sub/proxy.yaml"
  }
  sos_data = {
      "key": "sos",
      "interval": 86400,
      "url": f"https://SOS.CMLiussss.net/auto"
  }
  ripaojiedian_data = {
      "key": "ripaojiedian",
      "interval": 43200,
      "url": f"https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/clash"
  }
  free_list = [ "abshare", "abshare3", "mkshare3", "mksshare", "tolinkshare2", "toshare5" ]
  for it in free_list:
    add_subscript_link([{
      "key": it,
      "interval": 900,
      "url": f"https://raw.githubusercontent.com/mai19950/free_nodes/refs/heads/main/sub/clash/{it}.yaml"
    }], f"{it}.yaml")

  add_subscript_link([free_data], "free.yaml")
  add_subscript_link([sos_data], "sos.yaml")
  add_subscript_link([ripaojiedian_data], "ripaojiedian.yaml")
  add_subscript_link([git_data], "git.yaml")

  add_subscript_link([free_data, sos_data, ripaojiedian_data], "all.yaml")


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

