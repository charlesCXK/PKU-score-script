# --*-- encoding: utf-8 --*--
# 查询成绩

import re
import random
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

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

def message(key):
    html = getPage(key)
    
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

if __name__ == "__main__":
    query = 0
    while(1):
        query += 1
        time.sleep(random.uniform(0.88, 1.58))
        print("第 {} 次查询".format(query))
        message(key = 'http://dean.pku.edu.cn/student/new_grade.php?PHPSESSID=')