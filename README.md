
## Tornado Tool Bags
针对Tornado框架做了一个封装，包括不仅限于请求路由注册、日志打印、中间件、服务心跳、
定时任务、异常处理、异步GET/POST请求、数据库（MySQL/MongoDB/Redis）、邮件发送、
validator、工具类等功能。

## Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [HTTP Handler Route](#http-handler-route)
- [Change Logs](#change-logs)


#### Installation
```
    pip install tbag
```


#### Quick Start
> [example code](examples/quickstart)

* 创建配置文件 `config.py`
    ```text
    # -*- coding:utf-8 -*-
    
    """ 服务运行配置项
    """
    HTTP_PORT = 8080 # Http服务监听端口
    ```
    > 配置文件指定 `HTTP_PORT` 为8080，如果不指定，默认为10000

* 初始化并启动服务 `main.py`
    ```text
    # -*- coding:utf-8 -*-
    
    from tbag.core.context import TornadoContext
    
    
    def main():
        """ 启动程序
        """
        config_module = 'config'
    
        # 初始化 & 启动io loop
        TornadoContext(config_module).start()
    
    
    if __name__ == '__main__':
        main()
    ```

* 启动服务
    ```text
        python main.py
    ```


#### HTTP Handler Route
> [example code](examples/router)

* 配置文件中增加 `HANDLER_PATHES`
    ```text
    HANDLER_PATHES = ['api']
    ```
    > 配置文件中指定 `HANDLER_PATHES` 为 `['api']`，是一个列表，列表里放的是被 `@route` 装饰的 `RequestHandler` 模块；
    
    > 其中 `HANDLER_PATHES` 列表可指定任意多个模块；
    

* 创建模块文件 `api.py`
    ```text
    # -*- coding:utf-8 -*-
    
    from tbag.utils.routes import route
    from tbag.core.web import WebHandler
    from tbag.utils import log as logger
    
    
    @route('/api/test', 'api.test')
    class TestHandler(WebHandler):
    
        async def get(self, *args, **kwargs):
            logger.info('test handler GET:', self.request.path, caller=self)
            result = {'ok': 1}
            self.do_success(result)
    
        async def post(self, *args, **kwargs):
            body = self.get_body()
            logger.info('test handler POST:', self.request.path, 'body:',  body, caller=self)
            result = {'ok': 1}
            self.do_success(result)
    
        async def put(self, *args, **kwargs):
            body = self.get_body()
            logger.info('test handler PUT:', self.request.path, 'body:',  body, caller=self)
            result = {'ok': 1}
            self.do_success(result)
    
        async def patch(self, *args, **kwargs):
            body = self.get_body()
            logger.info('test handler PATCH:', self.request.path, 'body:',  body, caller=self)
            result = {'ok': 1}
            self.do_success(result)
    ```
    > `@route` 装饰器在 [routers.py](tbag/utils/routes.py)

* 启动服务
    ```text
        python main.py
    ```


#### Change Logs
* [Change Logs](docs/change_logs.md)
