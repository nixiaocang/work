###新增第三方库
```
numpy==1.15.0
pandas==0.23.4
psycopg2==2.7.5
supervisor==3.3.4
```

###supervisor相关配置
####如果需要修改路径相关配置 可以将 `/root/work/log` 替换为目标路径
####同时修改baidu.sh中的supervisor_pid的路径配置


###启动方式
```
cd $project
./baidu.sh start
```
###启动成功
```
baidu_server                     RUNNING   pid 30177, uptime 0:00:02
```

###重启服务
```
cd $project
./baidu.sh restart
```

###停止服务
```
cd $project
./baidu.sh stop
```

###问题排查
* 到数据库找到task_id
* cd $project
* grep task_id baidu_runtime.log
* 会显示出本次任务执行的全部日志记录
* 相应的错误堆栈信息也会显示出来
