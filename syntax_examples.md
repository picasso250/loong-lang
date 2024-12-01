# Loong 解释器语法示例

## 变量赋值
```plaintext
let a = 10;
let b = 3.14;
```

## 字符串
```plaintext
let c = "Hello, " + "world!";
```

## 条件运算符
```plaintext
let result = (a + b > 12 ? "Yes" : "No") + ", " + c;
```

## 多变量声明
```plaintext
let [x, y, z] = [1, 2, 3];
```

## 函数定义
```plaintext
fun sum(x, y):
    x + y
end
```

## 函数调用
```plaintext
let result = sum(a, b);
```

## 列表
```plaintext
let my_list = [1, 2, 3, 4, 5];
let first_element = my_list[0];  # 访问第一个元素
```

## 字典
```plaintext
let my_dict = {key1: "value1", key2: "value2"};
let value = my_dict["key1"];      # 访问字典值
```

## 条件表达式
```plaintext
let result = a > 10 ? "Greater" : "Smaller";
```

## 逻辑表达式
```plaintext
let result = (a > 10 and b < 5) or c == "Hello";
```
