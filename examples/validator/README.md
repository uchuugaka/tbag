#### Validator

在很多时候需要对数据做格式转换或格式校验，validator.py提供了python基础数据格式的转换或校验功能。

* 导入模块
```text
	from tbag.utils import validators
```

* 函数介绍
	- _bool_field(data, field=None, required=True)_  
		`bool`类型数据检查或转换
		```text
		flag = validators.bool_field("true")   # 返回 flag = True
		flag = validators.bool_field({"x": "false"}, "x")   # 返回 flag = False
		flag = validators.bool_field({"x": "false"}, "y")   # raise `exceptions.ValidationError`
		flag = validators.bool_field({"x": "false"}, "y", False)   # 返回 flag = None
		```
	- _int_field(data, field=None, required=True)_  
        `int`类型数据检查或转换
        ```text
        count = validators.int_field("123")   # 返回 count = 123
        count = validators.int_field({"x": 123}, "x")   # 返回 count = 123count = 123
        count = validators.int_field({"x": 123}, "y")   # raise `exceptions.ValidationError`
        count = validators.int_field({"x": "123"}, "y", False)   # 返回 count = None
        ```
    > 下边函数用法类似  
    - _float_field(data, field=None, required=True)_
    - _string_field(data, field=None, required=True)_
    - _list_field(data, field=None, required=True)_
    - _dict_field(data, field=None, required=True)_


* demo `api.py`
    ```text
	# -*- coding:utf-8 -*-
	
	from tbag.utils import validators
	from tbag.utils.routes import route
	from tbag.core.web import WebHandler
	from tbag.utils import log as logger
	
	
	@route('/api/test', 'api.test')
	class TestHandler(WebHandler):
	
	    async def _get_(self, *args, **kwargs):
	        page = validators.int_field(self.query_params, 'page')
	        logger.info('test handler GET:', self.request.path, 'page:', page, caller=self)
	        result = {'ok': 1}
	        self.do_success(result)
	
	    async def _post_(self, *args, **kwargs):
	        info = validators.dict_field(self.data, 'info')
	        logger.info('test handler POST:', self.request.path, 'info:',  info, caller=self)
	        result = {'ok': 1}
	        self.do_success(result)
    ```
    > 启动服务 `python main.py`  
    - 测试GET请求
	    ```text
		curl http://127.0.0.1:10000/api/test?page=33
		```
		> 日志打印: I [2018-03-23 11:36:09,953] [TestHandler.\_get_] [-] test handler GET: /api/test page: 33
	- 测试POST请求
		```text
		curl http://127.0.0.1:10000/api/test -X POST -d '{"info": {"name": "huangtao"}}'
		```
		> 日志打印: I [2018-03-23 11:37:40,388] [TestHandler.\_post_] [-] test handler POST: /api/test info: {'name': 'huangtao'}
