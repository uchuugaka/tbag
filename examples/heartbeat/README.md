#### Heartbeat & Tasks

在程序启动之前，可以注册某些固定间隔时间执行的任务，比如每10秒钟输出一行日志。

* 创建任务函数
	```text
	# -*- coding:utf-8 -*-
	
	from tbag.utils import log as logger
	
	
	def do_something(x, y, *args, **kwargs):
	    hb_count = kwargs.get('heart_beat_count', 0)
	    logger.debug('heart_beat_count:', hb_count)
	
	    if hb_count % 10 == 0:
	        logger.info('do something here every 10 seconds.')
            logger.info("x:", x, "y:", y)
	```
	> 函数被成功注册之后，服务内部每秒钟执行一次，可以依据 `heart_beat_count` 服务心跳来判断间隔，`heart_beat_count`
	> 每秒自加1；

* 注册任务函数
	```text
	# -*- coding:utf-8 -*-
	
	from tbag.core.context import TornadoContext
	
	
	def main():
	    config_module = 'config'
	
	    # 注册定时间隔任务
	    from tbag.core.heartbeat import heartbeat
	    import tasks
	    heartbeat.register(tasks.do_something, "today", "happy")
	
	    TornadoContext(config_module).start()
	
	
	if __name__ == '__main__':
	    main()
	```
	> 注册任务函数，需要在服务启动之前。
