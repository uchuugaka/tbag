
## Tornado框架工具包


#### Installion
```
    pip install tbag
```


#### Change Logs:

**2017/12/18**:
```
    Version: 1.2.3
    1. 增加web app初始化;
```

**2017/12/17**:
```
    Version: 1.2.2
    1. 删除tbag.core.web_base模块，新模块更新名字为tbag.core.web;
    2. 修改MYSQL配置参数user为username;
    3. 取消TornadoContext初始化参数传入方式，改为传入setting_module;
    4. 增加HTTP请求中间件;
```

**2017/12/12**:
```
    Version: 1.2.1
    1. 修改心跳日志打印为每5秒一次;
    2. 初始化参数去除port;
    3. 修改基类名DBBase为MongoDBBase;
    4. 日志消息里增加session_id;
```
