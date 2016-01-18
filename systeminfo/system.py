# -*- coding: utf-8 -*-
import psutil
import datetime
mem = psutil.virtual_memory()

print "================================================"
print "物理内存总大小  : " + str(mem.total)
print "已使用物理内存  : " + str(mem.used)
print "空闲的物理内存  : " + str(mem.free)
print "SWAP分区信息   : " + str(psutil.swap_memory())
print "================================================"
print "CPU详细信息:   :  " + str(list(psutil.cpu_times(percpu=True)))
print "用户的CPU时间比 : " + str(psutil.cpu_times().user)
print "CPU的逻辑个数   : " + str(psutil.cpu_count())
print "CPU的物理个数   : " + str(psutil.cpu_count(logical=False))
print "================================================"
print "磁盘完整信息    :" + str(psutil.disk_partitions())
print "'/'分区使用情况 :" + str(psutil.disk_usage('/'))
print "磁盘IO总信息     :" + str(psutil.disk_io_counters())
print "磁盘IO单硬盘信息  :" + str(psutil.disk_io_counters(perdisk=True))
print "================================================"
print "网络总IO信息     :" + str(psutil.net_io_counters())
print "每个网络接口信息  :" + str(psutil.net_io_counters(pernic=True))
print "================================================"
print "当前登录系统的用户信息: " + str(psutil.users())
print "开机时间: " + str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))