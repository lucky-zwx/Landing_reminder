import smtplib
from email.mime.text import MIMEText
import datetime
import getpass
# 可以封装成函数，方便 Python 的程序调用
import socket


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
msg_from = 'zhuwx1998@qq.com'  # 发送方邮箱
passwd = 'uzbmnbixxxxxxx'  # 填入发送方邮箱的授权码
msg_to = '794355xxx@qq.com'  # 收件人邮箱
subject = "服务器登陆提醒"  # 主题
mail_msg = """
<h1 style="text-align:center;">
        <strong></strong>服务器登陆提醒
</h1>
<p style="text-align:center;">
        🚩小旋风来报！！！
</p>
<p style="text-align:center;">
        大王不好啦，咱得服务器有人登录了🔐
</p>
<p style="text-align:center;">
    登录用户：
""" + str(getpass.getuser()) + """</p>""" + \
           """<p style="text-align:center;">
               登录IP：""" + get_host_ip() + """</p>""" + \
           """<p style="text-align:center;">
           登录时间：""" + now_time + """</p>"""

msg = MIMEText(mail_msg, 'html', 'utf-8')
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to
try:
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())
    print("发送成功")
except Exception:
    print("发送失败")
finally:
    s.quit()
