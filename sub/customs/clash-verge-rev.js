// Define main function (script entry)
const global = [
  // 🌏 全球加速
  "DOMAIN-SUFFIX,yfsp.tv",
  "DOMAIN-SUFFIX,pipecdn.vip",
  "DOMAIN,xslist.org",
  "DOMAIN,tktube.com",
  "DOMAIN,javdb.com",
  "DOMAIN,www.pexels.com",
  "DOMAIN-KEYWORD,premium-beauty",
  "DOMAIN,www.javlibrary.com",
  "DOMAIN-KEYWORD,javtrailers",
  "DOMAIN-KEYWORD,javlibrary",
  "DOMAIN-KEYWORD,missav",
  "DOMAIN-KEYWORD,7mmtv",
  "DOMAIN,img.supjav.com",
  "DOMAIN,supjav.com",
  "DOMAIN,avbebe.com",
  "DOMAIN-SUFFIX,mai9900.dpdns.org",
];

const select = [
  // 🚀 手动切换
  "DOMAIN-SUFFIX,2babes.com",
  "DOMAIN,emturbovid.com",
  "DOMAIN,stbhg.click",
  "DOMAIN,lk1.supremejav.com",
  "DOMAIN,javclan.com",
  "DOMAIN-SUFFIX,milocdn.com",
  "DOMAIN,ryderjet.com",
  "DOMAIN,hjd2048.com",
  "DOMAIN,mmvh01.xyz",
  "DOMAIN,mmsi01.xyz",
  "DOMAIN,fc2stream.tv",
  "DOMAIN-SUFFIX,cdn-centaurus.com",
  "DOMAIN-KEYWORD,javhoo",
  "DOMAIN-KEYWORD,sehuatang",
];

const direct = [
  // DIRECT
  "DOMAIN,javdb524.com",
  "DOMAIN,javdb456.com",
  "DOMAIN,gitlab.hk",
  "DOMAIN-SUFFIX,mongodb.com",
  "DOMAIN-KEYWORD,serv00",
  "DOMAIN-SUFFIX,tapecontent.net",
  "DOMAIN-KEYWORD,streamtape",
  "DOMAIN-SUFFIX,xunlei.com",
  "DOMAIN-SUFFIX,subtitlecat.com",
  "DOMAIN-SUFFIX,88cdn.com",
  "DOMAIN-KEYWORD,gcalenpjmijncebpfijmoaglllgpjag",
  "DOMAIN-SUFFIX,tampermonkey.net",
  "DOMAIN-SUFFIX,jdbstatic.com",
];

const reject = [
  // REJECT
  "DOMAIN-SUFFIX,ad-nex.com",
];

function main(config, profileName) {
  // 把旧规则合并到新规则后面(也可以用其它合并数组的办法)
  let oldRules = config["rules"];
  const prependRule = [].concat(
    global.map(it => (it += ",🌏 全球加速")),
    select.map(it => (it += ",🚀 手动切换")),
    direct.map(it => (it += ",DIRECT")),
    reject.map(it => (it += ",REJECT"))
  );
  config["rules"] = prependRule.concat(oldRules);
  return config;
}
