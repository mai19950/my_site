# Yaml

```yaml
proxy-groups:
  - {name: 🇭🇰 香港节点, type: url-test, lazy: true,  url: http://www.gstatic.com/generate_204, interval: 300, use: [Subscribe], filter: "港|HK|(?i)Hong" }
```

这个 Clash 配置项定义了一个名为 `🇭🇰 香港节点` 的代理组，它的类型是 `url-test`，并且包含了一些特定的配置。下面是对每一项的详细解释：

- `name: 🇭🇰 香港节点`:
  - 定义了这个代理组的名称，方便在其他策略组或规则中引用。这个组的目的是筛选并测试来自名为 `Subscribe` 的 `proxy-providers` 中包含特定关键词的香港节点。
- `type: url-test`:
  - 指定了这个代理组的类型为 `url-test`。`url-test` 策略组会定期（由 `interval` 控制）选择 `proxies` 列表中的每个代理节点，并向指定的 `url` 发送 `HTTP` 请求以测试其延迟和可用性。最终，这个策略组会选择延迟最低且可用的节点作为其出口。
- `lazy: true`:
  - 启用懒加载模式。这意味着只有当这个代理组被其他策略组实际使用时，Clash 才会对其包含的代理节点进行延迟测试。如果这个代理组一直没有被用到，就不会进行测试，从而节省资源。
- `url: http://www.gstatic.com/generate_204`:
  - 指定了 `url-test` 策略组用于测试代理节点延迟和可用性的目标 URL。`http://www.gstatic.com/generate_204` 是 Google 提供的一个非常轻量级的、通常响应速度很快的 URL，常用于网络连通性测试。
- `interval: 300`:
  - 设置了 `url-test` 策略组进行延迟测试的频率，单位是秒。这里 `300` 秒表示每隔 `5` 分钟，Clash 就会对这个代理组中的节点进行一次延迟测试。
- `use: [Subscribe]`:
  - 指定了这个 `url-test` 策略组所使用的代理节点来源。`Subscribe` 这里不是指 `proxies` 字段中直接定义的节点，而是指一个名为 `Subscribe` 的 `proxy-providers`。
  - 这意味着 Clash 会从名为 `Subscribe` 的 `proxy-providers` 中获取动态生成的代理节点列表，并对这些节点进行延迟测试。你需要在 `proxy-providers` 部分配置名为 `Subscribe` 的订阅信息，Clash 才能知道从哪里获取节点。
- `filter: "港|HK|(?i)Hong"`:
  - 这是一个过滤器，用于在 `Subscribe` 提供的代理节点列表中，只选择名称中包含特定关键词的节点。
  - `"港|HK|(?i)Hong"` 是一个正则表达式:
    - `港`: 匹配节点名称中包含 "港" 字的节点。
    - `|`: 表示逻辑或的关系。
    - `HK`: 匹配节点名称中包含 "HK" 这两个连续字符的节点。
    - `(?i)`: 表示不区分大小写。
    - `Hong`: 匹配节点名称中包含 "Hong" 这个字符串（不区分大小写）的节点。
  - 因此，这个过滤器会筛选出名称中包含 "港"、"HK" 或 "Hong"（不区分大小写）的代理节点，这些通常是香港的节点。

### `type`的值

1. `select`: 手动选择代理。当策略命中这个策略组时，Clash 客户端会提供一个可供用户选择的代理列表。
2. `url-test`: 自动选择延迟最低的可用代理。Clash 会定期测试列表中的每个代理到指定 URL 的延迟，并选择延迟最低且成功的代理。你提供的配置中 `🇭🇰` 香港节点 就是这个类型。
3. `fallback`: 按照代理列表的顺序尝试连接，直到找到一个可用的代理。如果列表中的第一个代理不可用，则尝试第二个，依此类推。
4. `load-balance`: 负载均衡。将连接均匀地分配到列表中的多个可用代理上。通常需要配合特定的负载均衡算法。
5. `relay`: 隧道/中继。将流量依次通过列表中的多个代理服务器转发。可以用于隐藏真实 IP 或访问特定网络。注意：目前 Clash 的 relay 类型不支持 UDP。
6. `script`: 使用自定义的 JavaScript 或 Starlark 脚本来选择代理。这提供了极高的灵活性，可以根据各种复杂的条件来选择代理。这是一个高级功能。

## `script` 类型的 `proxy-group` 要怎么操作

> `script` 类型的 `proxy-group` 是 Clash 中一个非常强大的高级特性，它允许你使用 JavaScript 或 Starlark 脚本来动态地选择代理。这为你提供了极高的灵活性，可以根据各种复杂的逻辑来决定使用哪个代理或哪些代理。

以下是如何操作 `script` 类型的 `proxy-group` 的详细说明：

### 基本语法

```yaml
proxy-groups:
  - name: <你的代理组名称>
    type: script
    script: |
      <你的脚本代码>
    interval: <执行间隔 (可选，秒)>
    timeout: <脚本执行超时时间 (可选，秒)>
    params:
      <自定义参数 (可选)>
```

> `script`: 包含你的脚本代码。你可以直接将代码写在这里（多行需要使用 `|`），也可以通过 `url` 或 `path` 引用外部脚本文件。

```yaml
script: |
  function selectProxy() {
    // 你的选择逻辑
    return "节点名称"; // 返回一个节点名称或一个包含节点名称的数组
  }

script:
  url: "https://example.com/my_script.js"

script:
  path: "./scripts/my_script.js"
```

### 示例 (JavaScript - 基于节点名称过滤)

```yaml
proxy-groups:
  - name: 🇭🇰 香港节点 (Script)
    type: script
    script: |
      function selectProxy() {
        const proxies = $config.proxies;
        const hongKongNodes = [];
        const filterRegex = /(港|HK|(?i)Hong)/;
        for (const proxy of proxies) {
          if (proxy.name && filterRegex.test(proxy.name)) {
            hongKongNodes.push(proxy.name);
          }
        }
        if (hongKongNodes.length > 0) {
          // 返回第一个匹配到的香港节点
          return hongKongNodes[0];
          // 或者返回所有匹配到的香港节点，让用户手动选择
          // return hongKongNodes;
        } else {
          return "DIRECT"; // 如果没有匹配到，返回 DIRECT
        }
      }
```

### 示例 (JavaScript - 基于延迟选择)

```Yaml
proxy-groups:
  - name: 自动选择 (Script)
    type: script
    script: |
      async function testLatency(proxyName) {
        try {
          const startTime = Date.now();
          const response = await $http.get({ url: "http://www.gstatic.com/generate_204", proxy: proxyName, timeout: 3000 });
          if (response.status === 204) {
            return Date.now() - startTime;
          }
        } catch (error) {
          return Infinity; // 表示连接失败
        }
        return Infinity;
      }

      async function selectProxy() {
        const proxies = $config.proxies;
        const latencyResults = [];
        for (const proxy of proxies) {
          const latency = await testLatency(proxy.name);
          latencyResults.push({ name: proxy.name, latency: latency });
        }
        latencyResults.sort((a, b) => a.latency - b.latency);
        // 返回延迟最低且成功的节点名称
        for (const result of latencyResults) {
          if (result.latency !== Infinity) {
            return result.name;
          }
        }
        return "DIRECT"; // 如果所有节点都不可用
      }

      async function main() {
        return await selectProxy();
      }
    interval: 600 # 每 10 分钟重新测试延迟
```

### 示例

```yaml
script-filter-hk: &filter_hk_script |
  function selectProxy() {
    const proxies = $config.proxies;
    const hongKongNodes = [];
    const filterRegex = /(港|HK|(?i)Hong)/;
    for (const proxy of proxies) {
      if (proxy.name && filterRegex.test(proxy.name)) {
        hongKongNodes.push(proxy.name);
      }
    }
    if (hongKongNodes.length > 0) {
      return hongKongNodes[0];
    } else {
      return "DIRECT";
    }
  }

proxy-groups:
  - name: 🇭🇰 香港节点 (Script 1)
    type: script
    script: *filter_hk_script
  - name: 🇭🇰 香港节点 (Script 2 - 略有不同)
    type: script
    script: |
      function selectProxy() {
        const proxies = $config.proxies;
        const hongKongNodes = [];
        const filterRegex = /(香港|Hong Kong)/i; // 不同的过滤规则
        for (const proxy of proxies) {
          if (proxy.name && filterRegex.test(proxy.name)) {
            hongKongNodes.push(proxy.name);
          }
        }
        return hongKongNodes.length > 0 ? hongKongNodes : ["DIRECT"];
      }
```
