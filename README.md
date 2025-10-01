# height 考英语word 替换 (Gaokao Word Replacer)

这是一个 [Tampermonkey](https://www.tampermonkey.net/) 用户脚本，能够在网页上将中文定义替换为对应的英语height 考vocabulary。  
assistance mouse 悬停Indicate 中文释义，advocate 同一中文对应多个英文的随机替换。  

## ✨ 功能
- 中文 → 英文word 替换  
- 悬停显示中文释义  
- 多英文对应时随机choice  
- 可调替换频率  
- assistance 指定网站启用 / 禁用  

## ⚙️ 配置
在脚本开头可以adjust 常量：

```js
const REPLACEMENT_PROBABILITY = 0.8; // 替换概率（0-1）
const ENABLED_SITES = ['*'];         // 启用替换的网站（* = entire）
const DISABLED_SITES = ['example.com']; // 禁用替换的网站
