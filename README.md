# Landing_reminder
服务器登录邮箱提醒
本次更新了验证登录，为二次验证
[![kncC9J.md.png](https://s2.ax1x.com/2019/01/26/kncC9J.md.png)](https://imgchr.com/i/kncC9J)

使用方法：
### **根据自己的服务器修改一下main.py中的域名** ###
在/etc/ssh目录下新建名为sshrc的文件，类容如下：

```
#!/bin/bash
trap '' SIGUSR2
trap '' SIGUSR1
trap '' SIGTERM
trap '' SIGSTOP
trap '' SIGTTIN
trap '' SIGTSTP
trap '' SIGTTIN
trap '' SIGTTOU
trap '' SIGCHLD
trap '' SIGINT
trap '' INT

/usr/bin/python3.5(版本根据实际情况使用) /root/sshrc(这个文件为main.py,到时候用改一下名就好) > /root/log.txt
```

![knFdlF.png](https://s2.ax1x.com/2019/01/25/knFdlF.png)
