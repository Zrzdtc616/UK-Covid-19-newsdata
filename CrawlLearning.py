# coding:utf-8

# 引入相关模块
#from bs4 import BeautifulSoup
#import requests

# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys

"""
类说明:获取卫报有关冠状病毒新闻的元数据
Parameters:
    无
Returns:
    无
Modify:
    2020-04-13
"""

class downloader(object):

    def __init__(self):
        self.server = 'https://www.theguardian.com/uk'
        self.target = 'https://www.theguardian.com/world/coronavirus-outbreak/all'
        self.titles = []            #存放新闻标题
        self.urls = []            #存放新闻链接
        self.nums = 0            #新闻数

    """
    函数说明:获取新闻链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2020-04-13
    """
    def get_download_url(self):
        req = requests.get(url = self.target)
        html = req.text
        div_bf = BeautifulSoup(html, 'html.parser')
        div = div_bf.find_all('div', class_ = 'fc-container__body')
        a_bf = BeautifulSoup(str(div[0]), 'html.parser')
        a = a_bf.find_all('a', 'u-faux-block-link__overlay')
        self.nums = len(a)
        for each in a:
            self.titles.append(each.get_text())
            self.urls.append(each.get('href'))

    """
    函数说明:获取新闻作者元数据
    Parameters:
        target - 下载连接(string)
    Returns:
        author - 新闻作者(string)
    Modify:
        2020-04-13
    """
    def get_authors(self, target):
        req = requests.get(url = target)
        html = req.text
        div_bf = BeautifulSoup(html, 'html.parser')

        authors = []
        author = div_bf.find_all('span', itemprop = 'name')
        
        for each in author:
            authors.append(each.get_text())
        return authors


    """
    函数说明:将爬取的内容写入文件
    Parameters:
        titles - 新闻标题名称(string)
        path - 当前路径下,小说保存名称(string)
        authors - 作者名称(string)
    Returns:
        无
    Modify:
        2020-04-13
    """
    def writer(self, titles, path, authors):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(titles)
            f.writelines(authors)
            f.write('\n\n')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《一年永恒》开始下载：')
    for i in range(dl.nums):
        #dl.writer(dl.titles[i], '新闻数据.txt', dl.get_authors(dl.urls[i]))
        #sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums) + '\r')
        #sys.stdout.flush()
        #print(dl.titles[i])
        #print(dl.urls[i])
        #print(dl.get_authors(dl.urls[i]))
        print(i)
        #系统一直报错index out of range，我分析了一圈觉得原因应该是在于这个for循环里
        #range(dl.nums)、dl.titles[i]、dl.get_authors(dl.urls[i])
        #因为收集到的数据不准确，dl.nums的数量可能会超过dl.titles和dl.urls，导致这个问题
        #总之感觉这个错误常常出现在for循环里
        #第1种可能情况：list[index]index超出范围
        #第2种可能情况：list是空值就会出现IndexError: list index out of range
        #第二种情况尤为难以排除错误
    print('《一年永恒》下载完成')
    #问题1: 标题和作者之间没有空格
    #问题2: 作者和作者之间没有空格
    #问题3: 原网站一个作者名称如果分两行写可能名字中间会出现-，因此爬取出的作者名也含有-，需要删除
'''
#翻页
titles = []
urls = []
for i in range(2):
    target = 'https://www.theguardian.com/world/coronavirus-outbreak?page={}'.format(i + 1)
    req = requests.get(url = target)
    html = req.text
    div_bf = BeautifulSoup(html, 'html.parser')
    div = div_bf.find_all('div', class_ = 'fc-container__body')
    a_bf = BeautifulSoup(str(div[0]), 'html.parser')
    a = a_bf.find_all('a', 'u-faux-block-link__overlay')
    for each in a:
        titles.append(each.get_text())
        urls.append(each.get('href'))
'''


'''
#连接、创建数据库，添加表格
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="wsgtcdddtc",
  database="mydatabase"
)
#之前连接一直不成功，显示SyntaxError: invalid syntax
#结果是缩进的问题，这里必须缩进2个空格，不能按tab
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE theguarnews (id INT AUTO_INCREMENT PRIMARY KEY, Titles VARCHAR(255), Urls VARCHAR(255), Author1 VARCHAR(255), Author2 VARCHAR(255), Time VARCHAR(255), Description VARCHAR(700))")

sql = "INSERT INTO theguarnews (Titles, Urls) VALUES (%s, %s)"
for i in range(nums):
    val = (titles[i], urls[i])
    mycursor.execute(sql, val)
    mydb.commit()
mycursor.execute("SELECT * FROM theguarnews")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)

#sql = "TRUNCATE TABLE theguarnews"
#mycursor.execute(sql)
#mydb.commit()
#以上#中的内容是清空表格，且id从1开始计算
#如果用DELETE的话，id不会重新从1开始，而是接着之前的数据id递增
'''

'''
#爬取标题、作者、简介描述和发表时间
if __name__ == "__main__":
    #target = 'https://www.theguardian.com/world/2020/apr/13/coronavirus-uk-map-how-many-confirmed-cases-are-there-in-your-area'
    target = 'https://www.theguardian.com/commentisfree/2020/apr/12/the-guardian-view-on-labours-task-reading-the-signs-of-the-times'
    req = requests.get(url = target)
    html = req.text
    div_bf = BeautifulSoup(html)
    
    #head = div_bf.find_all('h1', class_ = 'content__headline')
    author = div_bf.find_all('header', class_ = 'content__head')
    #descri = div_bf.find_all('div', class_ = 'tonal__standfirst u-cf')
    #time = div_bf.find_all('header', class_ = 'content__head')
    
    #head_bf = BeautifulSoup(str(head[0]))
    #head0 = head_bf.find_all('h1')
    #print(head_bf.text)
    author_bf = BeautifulSoup(str(author[0]))
    author0 = author_bf.find_all('span', itemprop = 'name')
    #descri_bf = BeautifulSoup(str(descri[0]))
    #descri0 = descri_bf.find_all('p')
    #time_bf = BeautifulSoup(str(time[0]))
    #time0 = time_bf.find_all('time', itemprop = "datePublished")
    
    #for each in head0:
        #print(each.get_text(), "\n")
    for each in author0:
        print(each.get_text(), "\n")
    #for each in descri0:
        #print(each.get_text(), "\n")
    #for each in time0:
        #print(each.get_text())
    
  

if __name__ == "__main__":
    #爬虫的第一步：获取整个网页的HTML信息
    target = 'https://www.theguardian.com/world/coronavirus-outbreak/all'
    req = requests.get(url = target)
    #requests.get()方法用于向服务器发起get请求
    #能够获得html网页数据，对应于HTTP中的GET
    #requests.get()方法必须设置的一个参数就是url
    #因为我们得告诉GET请求，我们的目标是谁，我们要获取谁的信息。
    #用这个方法可以获得了某网页的所有HTML信息，这就是一个最简单的爬虫实例
    html = req.text
    #我猜测上面的req是一个对象，html这个变量就是获取了req这个对象中的所有文字，即所有的html代码
    #可以用print(html)来查看这些文字

    #爬虫的第二步，解析HTML信息，提取我们感兴趣的内容
    #提取的方法有很多，例如使用正则表达式、Xpath、Beautiful Soup等。
    #对于初学者而言，最容易理解，并且使用简单的方法就是使用Beautiful Soup提取感兴趣内容。
    #在解析html之前，我们需要创建一个Beautiful Soup对象div_bf。
    #BeautifulSoup函数里的参数就是我们已经获得的html信息。
    div_bf = BeautifulSoup(html)
    #然后我们使用find_all方法，
    #获得html信息中所有class属性为fc-container--rolled-up-hide的div标签。
    #为什么不是class，而带了一个下划线呢？因为python中class是关键字，
    #为了防止冲突，这里使用class_表示标签的class属性，class_后面跟着的fc..就是属性值了。
    div = div_bf.find_all('div', class_ = 'fc-container__body')
    #find_all方法的第一个参数是获取的标签名，第二个参数class_是标签的属性，
    a_bf = BeautifulSoup(str(div[0]))
    #我们已经顺利匹配到我们关心的div中的内容，但是还有一些我们不想要的东西。
    #比如div标签名，br标签，以及各种空格。怎么去除这些东西呢？
    a = a_bf.find_all('a')
    for each in a:
        print(each.get_text(), each.get('href'), "\n")
    #type(a_bf)和type(div_bf)为<class 'bs4.BeautifulSoup'>
    #type(a)和type(div)为<class 'bs4.element.ResultSet'>
        
'''


