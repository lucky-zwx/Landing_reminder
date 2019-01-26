import multiprocessing
import smtplib
from email.mime.text import MIMEText
import datetime
import getpass
import socket
import signal
import os
import time
import random
import socket
import sys
from multiprocessing import Process


def signal_handler(signal, frame):
    print('您现在没有操作权限！！！')


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def handle_client(client_socket, auth, Close_i):
    """
    处理客户端请求
    """
    request_data = client_socket.recv(1024)
    mess = request_data.decode('utf-8')
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = "<h1>Python HTTP Test</h1>"
    if auth in mess:
        response_body = "<h1>Success</h1>"
        Close_i.value = 1

    response = response_start_line + response_headers + "\r\n" + response_body

    # 向客户端返回响应数据
    client_socket.send(bytes(response, "utf-8"))

    # 关闭客户端连接
    client_socket.close()


def send_mail(port):
    signal.signal(signal.SIGINT, signal_handler)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg_from = 'zhuwx1998@qq.com'  # 发送方邮箱
    passwd = 'uzbmnbilafxxxxxx'  # 填入发送方邮箱的授权码
    msg_to = '7943xxxxx@qq.com'  # 收件人邮箱
    subject = "服务器登陆提醒"  # 主题
    zhuwx = '123'
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
               登录时间：""" + now_time + """</p>""" + \
               """<p style="text-align:center;">
               点击此链接登录服务器: """ + "http://www.xiaoyuan666.com:" + str(port) + "/" + auth + """</p>"""

    msg = MIMEText(mail_msg, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        # print(auth)
    except Exception:
        print("发送失败")
    finally:
        s.quit()


def get_auth():
    auths = ""
    for i in range(0, 4):  # 定义循环4次，形成4位验证码。
        current = random.randint(0, 4)  # 定义一个随机0-4的一个范围，去猜i 的值。
        if current == i:  # 如果current 和i 的值一样
            current_code = random.randint(0, 9)  # 生成一个随机的数字
        else:  # 如果current和i 的值不一样
            current_code = chr(random.randint(65, 90))  # 生成一个随机的字母，这里一定要主义chr（）转换一下。
        auths += str(current_code)  # 将每次随机生成的值赋值给auth
    return auths


auth = get_auth()

if __name__ == "__main__":
    port = random.randint(1900, 2000)
    send_mail(port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Close_i = multiprocessing.Value("d", 0)
    while True:
        client_socket, client_address = server_socket.accept()
        # print("[%s, %s]用户连接上了" % client_address)
        # print(auth)
        handle_client_process = Process(target=handle_client, args=(client_socket, auth, Close_i))
        handle_client_process.daemon = True
        handle_client_process.start()
        handle_client_process.join()
        client_socket.close()
        if Close_i.value == 1.0:
            print('Success')
            # handle_client_process.close()
            server_socket.close()
            break
