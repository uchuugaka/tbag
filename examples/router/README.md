#### HTTP Handler Route

* 配置文件中增加 `HANDLER_PATHES`
    ```text
    HANDLER_PATHES = ['api']
    ```
    > 配置文件中指定 `HANDLER_PATHES` 为 `['api']`，是一个列表，列表里放的是被 `@route` 装饰的 `RequestHandler` 模块；  
      其中 `HANDLER_PATHES` 列表可指定任意多个模块；
    

* 创建模块文件 `api.py`
    ```text
    # -*- coding:utf-8 -*-
    
    from tbag.utils.routes import route
    from tbag.core.web import WebHandler
    from tbag.utils import log as logger
    
    
    @route('/api/test', 'api.test')
    class TestHandler(WebHandler):
    
	    async def _get_(self, *args, **kwargs):
	        logger.info('test handler GET:', self.request.path, caller=self)
	        result = {'ok': 1}
	        self.do_success(result)
	
	    async def _post_(self, *args, **kwargs):
	        body = self.get_body()
	        logger.info('test handler POST:', self.request.path, 'body:',  body, caller=self)
	        result = {'ok': 1}
	        self.do_success(result)
	
	    async def _put_(self, *args, **kwargs):
	        body = self.get_body()
	        logger.info('test handler PUT:', self.request.path, 'body:',  body, caller=self)
	        result = {'ok': 1}
	        self.do_success(result)
	
	    async def _patch_(self, *args, **kwargs):
	        body = self.get_body()
	        logger.info('test handler PATCH:', self.request.path, 'body:',  body, caller=self)
	        result = {'ok': 1}
	        self.do_success(result)
    ```
    > `@route` 装饰器在 [routers.py](../../tbag/utils/routes.py)  
      特别注意，在HTTP的方法名左右需要加一个下划线（eg. \_get_/\_post_），tornado默认的HTTP方法名(eg. get/post)将不会使用异常处理及中间件；

* 启动服务
    ```text
        python main.py
    ```
