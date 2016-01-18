# -*- coding: utf-8 -*-
import psutil

print "所有进程PID: " + str(psutil.pids())
#实例化一个Process(进程)对象,参数为一个进程的PID
p = psutil.Process(1626)
print p.name() #进程名
print p.exe() #进程bin路径
print p.cwd() #进程工作目录绝对路径
print p.status() #进程状态
print p.create_time() #进程创建时间,时间戳格式