# PKU-dean-自动查分脚本
### 介绍

北大学生使用的通过爬取dean实现的自动查分脚本，Python3

### 查分说明

打开 http://dean.pku.edu.cn/student/，用自己的账号密码**登陆**后右键“成绩查询”链接，复制链接地址，得到
http://dean.pku.edu.cn/student/new_grade.php?PHPSESSID={} 
这样的链接，花括号内为和自己个人密码相关的信息。然后用以下语句运行代码。

```shell
$ python3 query.py --url 你的带个人信息的链接
```

### 邮件提醒功能

```shell
$ $ python3 query.py --url 你的带个人信息的链接 --email 你的邮箱
```

### 其他

推荐在服务器中，使用 ***tmux*** 将程序挂在后台。