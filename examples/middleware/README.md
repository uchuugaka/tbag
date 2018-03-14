#### Middleware

* 配置文件中增加 `MIDDLEWARES`
    ```text
    MIDDLEWARES = ['middleware.TestMiddleware']
    ```

* 配置文件中指定 `HANDLER_PATHES` 是一个列表，列表里放的是继承自 `Middleware` 类的中间件。  
* Middleware 来自 `tbag.core.middleware` 模块，其中包含了两个函数 `prepare` 和 `finish`，其中：
	- `prepare` HTTP方法执行之前的准备工作
	- `finish` HTTP方法执行之后的清理工作
