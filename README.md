
## Tornado Tool Bags


#### Installation
```
    pip install tbag
```


#### Quick Start
> [example code for quick start.](examples/quickstart)

* 创建配置文件 `config.py`
    ```text
    # -*- coding:utf-8 -*-
    
    """ 服务运行配置项
    """
    HTTP_PORT = 8080 # Http服务监听端口
    ```

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



#### Change Logs
* [Change Logs](docs/change_logs.md)
