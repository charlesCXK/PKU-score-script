# --*-- encoding: utf-8 --*--
# 查询成绩

import re
import random
import requests
import time
from bs4 import BeautifulSoup

def getPage(url):
    headers = {"Referer":url,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
    r = requests.get(url, headers=headers, timeout=20)
    r.encoding = "utf-8"
    return r.text

def message(key):
    html = getPage(key)
    soup = BeautifulSoup(html, 'html.parser')

    pat = re.compile(r"(17-18[0-9]{9})([0-9]*|[A-Z])(.*?)([0-9]{1})([0-9]*\.[0-9]*)")
    gpa = re.compile(r"([0-9]*\.[0-9]*)")
    course_num = 0
    # 找到所有行
    tr = soup.find_all('tr')
    td = soup.find_all('td')        # 目前最后这学期（当前学期）的绩点

    for rr in tr:
        grade = str(rr.text)
        if grade.startswith("17"):          # 本学期的课程
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

if __name__ == "__main__":
    query = 0
    while(1):
        query += 1
        time.sleep(random.uniform(0.88, 1.58))
        print("第 {} 次查询".format(query))
        message(key = 'http://dean.pku.edu.cn/student/new_grade.php?')