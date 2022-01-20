# web-to-struct
Convert web data to json.  
将web数据格式化为json。

## Node
```jsonc
{
  "name": "",
  "map": [
    { "function": "", "kwargs": {} } // 内置函数，上一个的输出作为下一个的输入
  ],
  "children": [{}] // optional 子节点，结构同本结构。
}
```

### Functions
| Function 函数名 | Accepted Returns 可接受的上一个函数的返回类型 | Extra Args 额外的参数 | Returns 返回类型 | Description 描述 |
| --- | --- | --- | --- | --- |
| string-to-element | String | [feature] | Element | - |
| css | [String, Element] | css pattern | [Element, None] | - |
| xpath | [String, Element] | xpath pattern | Element | - |
| index | [Dict, Tuple] | pattern, eg."[1].x" | Any | - |
| text | Element | - | String | get all the pure strings (remove all HTML tags) inside the current elements |
| html | Element | - | String | get all the HTML strings inside the current element |
| attr | Element | attr_name | String | get the current element’s attribute value |
| regex | String | pattern | [String, Tuple] | regex match result |
| tuple-to-string | Tuple | pattern | String | use $1,$2,... to replace tuple elements, eg. "hello $1, $2" for tuple ("a", "b") returns "hello a, b" |
| json-parse | String | - | Dict | parse json string to dict |


### 其他行为
 - 返回值如果是list，且有children，则处理为返回值叉乘children
