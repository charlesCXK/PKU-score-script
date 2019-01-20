# --*-- encoding: utf-8 --*--
# 查询成绩

import re
import random
import requests
import time
import argparse
import smtplib

from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

'''
[description]
get the content of content
'''
def connect(url):
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(url)

    return driver 

def getPage(url):
    headers = {"Referer":url,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"}
    r = requests.get(url, headers=headers, timeout=20)
    r.encoding = "utf-8"
    return r.text

'''
[description]
邮件提醒功能
'''
def sendemail(target_email, content):
    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="tixishixi@163.com"    #用户名
    mail_pass="pkuscore2019"   #口令 

    sender = 'tixishixi@163.com'
    receivers = [target_email]  # 接收邮件，可设置为你的邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = "{}".format(sender)   # 发送者
    message['To'] = ",".join(receivers)       # 接收者
     
    subject = 'PKU-score-script'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def message(args, lesson_num):
    url = args.url
    html = getPage(url)
    
    # driver = connect(key)
    # iframe = driver.find_element_by_name('main')
    # driver.switch_to.frame(iframe)
    # table = driver.find_elements_by_tag_name('table')

    soup = BeautifulSoup(html, 'html.parser')

    pat = re.compile(r"(18-19[0-9]{9})([0-9]*|[A-Z])(.*?)([0-9]{1})([0-9]*\.[0-9]*)")
    gpa = re.compile(r"([0-9]*\.[0-9]*)")
    course_num = 0
    # 找到所有行
    tr = soup.find_all('tr')
    td = soup.find_all('td')        # 目前最后这学期（当前学期）的绩点

    for rr in tr:
        grade = str(rr.text)
        if grade.startswith("18"):          # 本学期的课程
            res = pat.findall(grade)
            if res:
                res = res[0]
                course_num += 1
                print("分数: {},  GPA:  {},  学分: {},  课程:{}".format(res[1], res[4], res[3], res[2]))
            '''
            res2 = gpa.findall(grade)
            if "当前学期平均绩点" in grade and res2:
                res2 = res2[0]
                print("当前学期GPA：{}".format(res2[0]))'''
    print("\n***************************************  一共 {} 门课程出分  ***************************************".format(course_num))
    print("***************************************  当前学期GPA：{}  ***************************************".format(td[-1].text))
    print('\n' * 2)

    if course_num != lesson_num:
        lesson_num = course_num

        if len(args.email) > 0:
            sendemail(args.email, '有新的成绩出分，本学期目前总绩点: {}'.format(td[-1].text))

    return lesson_num

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', default='', type=str, help = 'webpage url')
    parser.add_argument('--email', '-e', default='', type=str, help = 'your email address')
    args = parser.parse_args()

    query = 0
    lesson_num = 0      # 上一次出分的课程数
    while(1):
        query += 1
        time.sleep(random.uniform(0.88, 1.58))
        print("第 {} 次查询".format(query))
        lesson_num = message(args, lesson_num)