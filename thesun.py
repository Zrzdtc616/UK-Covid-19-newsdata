'''
# Import related modules
from bs4 import BeautifulSoup
import requests
import mysql.connector

# Get topics--------------------------------
def get_topics(soup):
    top = soup.find_all('div', class_ = 'tags tags--article')
    #create a list to store 5 topics
    topics = ['', '', '', '', '']
    if top == []:
        topics = ['', '', '', '', '']
    else:
        top_bf = BeautifulSoup(str(top[0]), 'html.parser')
        topic = top_bf.find_all('li', class_ = 'tags__item')
        topnum = len(topic)
        if topnum < 5:
            for i in range(0, topnum):
                # store topics
                topics[i] = topic[i].get_text()
            for i in range(topnum, 5):
                topics[i] = ''
        elif topnum >= 5:
            for i in range(0, 5):
                topics[i] = topic[i].get_text()
    return topics

# Get Classification C1, C2, C3------------------------------
def get_categories(soup):
    cate = soup.find_all('div', class_ = 'sun-container theme-main')
    if cate == []:
        C1 = ''
        C2 = ''
    else:
        cate_bf = BeautifulSoup(str(cate[0]), 'html.parser')
        cates = cate_bf.find_all('li', class_ = 'active')
        if len(cates) == 0:
            C1 = ''
        elif len(cates) == 1:
            C1 = cates[0].get_text()
            C2 = ''
        else:
            C1 = cates[0].get_text()
            C2 = cates[1].get_text()   
    return C1, C2

# Get Authors --------------------------------
def get_authors(soup):
    auth = soup.find_all('div', class_ = 'article__name-date')
    authors = ['', '', '', '']
    if len(auth) == 0:
        authors = ['', '', '', '']
    else:
        auth_bf = BeautifulSoup(str(auth[0]), 'html.parser')
        author = auth_bf.find_all('li', class_ = 'article__author-list')
        if len(author) == 0:
            authors = ['', '', '', '']
        elif len(author) == 1:
            authors[0] = author[0].get_text()
        elif len(author) == 2:
            authors[0] = author[0].get_text()
            authors[1] = author[1].get_text()
        elif len(author) == 3:
            authors[0] = author[0].get_text()
            authors[1] = author[1].get_text()
            authors[2] = author[2].get_text()
        else:
            authors[0] = author[0].get_text()
            authors[1] = author[1].get_text()
            authors[2] = author[2].get_text()
            authors[3] = author[3].get_text()
    if len(authors[0]) > 50:
        authors[0] = authors[0][0:50]
    if len(authors[1]) > 50:
        authors[1] = authors[1][0:50]
    if len(authors[2]) > 50:
        authors[2] = authors[2][0:50]
    if len(authors[3]) > 50:
        authors[3] = authors[3][0:50]
    return authors


# Get Publish Time------------------------------
def get_time(soup):
    tim = soup.find_all('div', class_ = 'article__name-date')
    if tim == []:
        times = ''
    else:
        tim_bf = BeautifulSoup(str(tim[0]), 'html.parser')
        time = tim_bf.find_all('li', class_ = 'article__published')
        if time == []:
            times = ''
        else:
            times = time[0].get_text()
    return times


# Get News Description------------------------------
def get_description(soup):
    des = soup.find_all('div', class_ = 'article__content')
    if des == []:
        descris = ''
    else:
        des_bf = BeautifulSoup(str(des[0]), 'html.parser')
        descri = des_bf.find_all('p', class_ = 'article__content--intro')
        if descri == []:
            descris = ''
        else:
            descris = descri[0].get_text()
    return descris

# Get News Content------------------------------
def get_content(soup):
    con = soup.find_all('div', class_ = 'article__content')
    cons = []
    if con == []:
        cons = ''
    else:
        con_bf = BeautifulSoup(str(con[0]), 'html.parser')
        content = con_bf.find_all('p')
        if content == []:
            cons = ''
        else:
            for i in content:
                cons.append(i.get_text())
            cons = ' '.join(cons) #将列表中的所有项合并成一个字符串，cons的类型为list
            #因为mysql中设置的content的长度是10000，超过一万导入的话会报错
            #所以如果超过10000，只截取前10000个字符。
            if len(cons) > 10000:
                cons = cons[0:9999]
    return cons


# Get All, Connect to MySQL------------------------------
def get_titleurl():
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="wsgtcdddtc",
      database="mydatabase"
    )
    mycursor = mydb.cursor()


    for i in range(700, 722): # from page 1 to 10
        target = 'https://www.thesun.co.uk/topic/coronavirus/page/{}/'.format(i)
        req = requests.get(url = target)
        html = req.text
        div_bf = BeautifulSoup(html, 'html.parser')
        a = div_bf.find_all('a', class_ = 'text-anchor-wrap')
        #a_bf = BeautifulSoup(str(div[0]), 'html.parser')
        #a = a_bf.find_all('a', 'u-faux-block-link__overlay')

        for each in a:
            try:
                titles = each.find('p').get_text().replace('\n','').replace('\t','')
                urls = each.get('href')
                headlines = ''
                headlines = each.find('h2').get_text()

                target0 = each.get('href')
                req0 = requests.get(url = target0)
                html0 = req0.text
                div_bf0 = BeautifulSoup(html0, 'html.parser')

                topresult = get_topics(soup = div_bf0)#topresult是一个有5个值的列表
                cateresult = get_categories(soup = div_bf0)#cateresult是一个元组
                authresult = get_authors(soup = div_bf0)
                timeresult = get_time(soup = div_bf0)
                desresult = get_description(soup = div_bf0)
                conresult = get_content(soup = div_bf0)
                sql = "INSERT INTO thesunnews (Titles, Urls, Headlines, Topic1, Topic2, Topic3, Topic4, Topic5, C1, C2, Author1, Author2, Author3, Author4, Time, Description, Content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (titles, urls, headlines, topresult[0], topresult[1], topresult[2], topresult[3], topresult[4], cateresult[0], cateresult[1], authresult[0], authresult[1], authresult[2], authresult[3], timeresult, desresult, conresult)
                mycursor.execute(sql, val)
                mydb.commit()
            except IndexError:
                pass
            except AttributeError:
                pass

# Main function----------------------------------------------

if __name__ == '__main__':
    #create table
    #sql = "CREATE TABLE thesunnews(id INT AUTO_INCREMENT PRIMARY KEY, Titles VARCHAR(255), Urls VARCHAR(255), Headlines VARCHAR(50), Topic1 VARCHAR(50), Topic2 VARCHAR(50), Topic3 VARCHAR(50), Topic4 VARCHAR(50), Topic5 VARCHAR(50), C1 VARCHAR(50), C2 VARCHAR(50), Author1 VARCHAR(50), Author2 VARCHAR(50), Author3 VARCHAR(50), Author4 VARCHAR(50), Time VARCHAR(50), Description VARCHAR(700), Content VARCHAR(10000))"
    #mycursor.execute(sql)
    get_titleurl()
'''

'''
nums = len(titles)
sql = "INSERT INTO theguarnews (Titles, Urls, Labelsers, Labelsecs, Author1, Author2, Author3, Author4, Time, Description) VALUES (%s, %s, %s, %s, %s, %s)"
for i in range(nums):
    val = (titles[i], urls[i], labelsers[i], labelsecs[i], authors1[i], authors2[i], authors4[i], authors4[i], times[i], descris[i])
    mycursor.execute(sql, val)
    mydb.commit()

mycursor.execute("SELECT * FROM thesunnews")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)

'''

#Export as excel file
import xlwt
import mysql.connector

row0 = ['Titles', 'Urls', 'Headlines', 'Topic1', 'Topic2', 'Topic3', 'Topic4', 'Topic5', 'C1', 'C2', 'Author1', 'Author2', 'Author3', 'Author4', 'Time', 'Description', 'Content']
book = xlwt.Workbook(encoding='utf-8')


#获取MYSQL中thesunnews表格中的所有数据
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="wsgtcdddtc",
    database="mydatabase"
    )
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM thesunnews")
myresult = mycursor.fetchall()


#获取MYSQL里面的数据字段名称
fields = mycursor.description

#注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
#cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
sheet = book.add_sheet('January', cell_overwrite_ok=True)
#“卫报数据”是这个sheet的名字，不是整个excel的名字

#写上字段信息
for field in range(0, len(fields)):
    sheet.write(0, field, fields[field][0])

# 获取并写入数据段信息
row = 1
col = 0
for row in range(1,len(myresult)+1):
    for col in range(0, len(fields)):
        sheet.write(row, col, u'%s' % myresult[row-1][col])

book.save("thesunnews.xls")#给表格命名并保存，这个时候“下载”文件夹中就会多出一个excel文件了～


#清空表格内容
#sql = "TRUNCATE TABLE thesunnews"
#mycursor.execute(sql)
#mydb.commit()
#mycursor.execute("TRUNCATE TABLE thesunnews")

#删除表格
#sql = "DROP TABLE thesunnews"
#mycursor.execute(sql)

'''
#连接数据库
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="wsgtcdddtc",
    database="mydatabase"
    )
mycursor = mydb.cursor()
mycursor.execute("TRUNCATE TABLE thesunnews")
mydb.commit()
#mycursor.execute("alter table theguarnews change Content Content varchar(10000) character set utf8mb4")
'''
