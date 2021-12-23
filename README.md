# web-to-struct
Convert web data to json.  
将web数据格式化为json。

----

## 思路
大体上沿用folk-api那套，再参考下yealico那套，整个Node结构出来先：

### Node
```jsonc
{
  "name": "",
  "css": "", // optional 对于Elem可用
  "xpath": "", // optional 对于Elem可用
  "index": "[1].x", // optional 下标，对于object/dict可用
  "map": [ // optional
    { "function": "", "args": "depend-on-function" } // 内置函数，上一个的输出作为下一个的输入
  ],
  "children": [{}] // optional 子节点，结构同本结构。
}
```

### Node Fields
| Field 字段 | Description 描述 |
| --- | --- |
| name | field name 字段名 |
| css | css selector, Element accepted |
| xpath | xpath selector, Element accepted |
| index | lookup in a Dict, Dict accepted, 字典下标。 eg. "[0]"返回第0个元素, "[0].key1"返回第0个元素的字典里的key1字段 |
| map | process for selected result, 结果的后处理 |
| children | child nodes, 子节点 |

**如果Node返回是的数组，则输出结果的此字段也为数组**

### Node Returns
 - Element
 - String
 - Tuple
 - Dict

### Functions
| Function 函数名 | Accepted Returns 可接受的上一个函数的返回类型 | Extra Args 额外的参数 | Returns 返回类型 | Description 描述 |
| --- | --- | --- | --- | --- |
| text | Element | - | String | get all the pure strings (remove all HTML tags) inside the current elements |
| html | Element | - | String | get all the HTML strings inside the current element |
| attr | Element | attr_name | String | get the current element’s attribute value |
| regex | String | pattern | String, Tuple | regex match result |
| tuple-to-string | Tuple | pattern | String | use $1,$2,... to replace tuple elements, eg. "hello $1, $2" for tuple ("a", "b") returns "hello a, b" |
| json-parse | String | - | Dict | parse json string to dict |
