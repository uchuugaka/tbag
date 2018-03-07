### Change Logs:


**2018/03/07**:
```
    Version: 1.3.2
    1. 引入Redis支持;
```

**2017/12/29**:
```
    Version: 1.3.1
    1. 跨域增加设置 Access-Control-Allow-Headers;
    2. 返回datetime类型时间转换为UTC时间;
    3. 引入asyncio;
```

**2017/12/29**:
```
    Version: 1.3.0
    1. 修复bug: 处理查询条件里_id的各种类型;
```

**2017/12/26**:
```
    Version: 1.2.9
    1. 修复bug: 引入被删除的模块;
```

**2017/12/22**:
```
    Version: 1.2.8
    1. 修复bug: 继承类默认msg和code失效;
    2.delete useless mudoles: tbag.utils.errors;
```

**2017/12/18**:
```
    Version: 1.2.4
    1. 增加datetime_help.py模块;
```

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
