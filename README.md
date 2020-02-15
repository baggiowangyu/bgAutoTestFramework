# bgAutoTestFramework
自动化测试框架，测试用例

## 框架说明

- 本框架目标是托管自动测试的

## 依赖的第三方库

- toml：配置文件读写库

```
pip install toml
pip install xlrd
pip install requests
pip install jsonpatch
```

## 测试用例模板

| 用例ID | 用例名称 | 接口路径 | 调用方法 | 重复次数 | Query参数 | Body参数 | 标准返回 | 
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | 测试用户登录 | /login | POST | 100 |  | {"username":"admin", "password":"12345"} | {"code": 200, "detail": "SUCCESS"} |
| 2 | 测试用户登出 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |
