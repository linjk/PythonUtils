# -*- coding: utf-8 -*-
# 2016/01/09 08:58:54
#
# 实现HTML格式的数据报表邮件

import smtplib
from email.mime.text import MIMEText

HOST = "smtp.qq.com"
SUBJECT = u"流量数据报表"
TO = "linjk121@163.com"
FROM = "3231047458@qq.com"

msg = MIMEText("""    #创建一个MIMEText对象,分别指定HTML内容,类型(文本或HTML),字母编码
            <table width="800" border="0" cellspacing="0" cellpadding="4">
                <tr>
                    <td bgcolor="#CECFAD" height="20" style="font-size:14px">数据<a href="www.baidu.com">More>></a></td>
                </tr>
                <tr>
                    <td bgcolor="#EFEBDE" height="100" style="font-size:13px">
                    1)日访问量:<font color=red>152433</font> 访问次数: 23651 数据流量: 504MB<br>
                    2)页面信息<br>
                    &nbsp;&nbsp;/index.php 42153<br>
                    &nbsp;&nbsp;/view.php 12153<br>
                    </td>
                </tr>
            </table>""", "html", "utf-8")
msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO

try:
    server = smtplib.SMTP()
    server.connect(HOST, "465") #465 or 587
    server.starttls()
    server.login("3231047458@qq.com", "shenzhennuli8")
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    print "邮件发送成功"
except Exception, e:
    print "Error: " + str(e)