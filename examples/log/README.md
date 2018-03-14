#### Log

* 配置文件中增加 `LOG`
    ```text
	LOG = {
		"level": "INFO",
		"path": "/var/log/test",
		"name": "test.log"
	}
    ```
    > `level` 日志级别（DEBUG/INFO），默认为 `DEBUG`  
      `path` 日志路径，默认为 `/tmp/logs`  
      `name` 日志名，默认为 `tbag.log`
        
* 日志文件按天分割，在每天凌晨 00:00 分割前一天的日志，并在文件名后追加当天日期为新的日志文件。 `eg: test.log.2018-01-01`    

* 日志打印有5个函数，使用方式如下:
	> from tbag.utils import log as logger  
	  logger.info(...)  
	  logger.debug(...)  
	  logger.warn(...)  
	  logger.error(...)  
	  logger.exception()  

* 传入参数中如果加入 `caller=self` 或 `caller=cls`，即可打印调用日志的类名及方法名 `ClassName.methodName`，默认只打印方法名。
	> logger.info("username", "test", caller=self)

* 如果配置文件中不指定 `LOG`，那么日志将直接打印到控制台。
