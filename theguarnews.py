'''
# Import related modules
from bs4 import BeautifulSoup
import requests
import mysql.connector


# Get keywords--------------------------------
def get_keywords(soup):
    key = soup.find_all('div', class_ = 'submeta__keywords')
    #create a list to store 10 keywords
    keywords = ['', '', '', '', '', '', '', '', '', ''] 
    if key == []:
        keywords = ['', '', '', '', '', '', '', '', '', '']
    else:
        key_bf = BeautifulSoup(str(key[0]), 'html.parser')
        keyword = key_bf.find_all('li', class_ = 'submeta__link-item')
        keynum = len(keyword)
        if keynum < 10:
            for i in range(0, keynum):
                # store keywords but delete blank space
                keywords[i] = keyword[i].get_text().replace('\n', '') 
            for i in range(keynum, 10):
                keywords[i] = ''
        elif keynum >= 10:
            for i in range(0, 10):
                keywords[i] = keyword[i].get_text().replace('\n', '')
    return keywords
# Get Classification C1, C2, C3------------------------------
def get_categories(soup):
    cate = soup.find_all('header', class_ = 'new-header')
    if cate == []:
        C1 = ''
        C2 = ''
        C3 = ''
    else:
        cate_bf = BeautifulSoup(str(cate[0]), 'html.parser')
        c1 = cate_bf.find_all('a', class_ = 'pillar-link--current-section')
        if c1 == []:
            C1 = ''
        else:
            C1 = c1[0].get_text().replace('\n', '')
        c2 = cate_bf.find_all('li', class_ = 'subnav__item--parent')
        if c2 == []:
            C2 = ''
        else:
            C2 = c2[0].get_text().replace('\n', '')
        c3 = cate_bf.find_all('a', class_ = 'subnav-link--current-section')
        if c3 == []:
            C3 = ''
        else:
            C3 = c3[0].get_text().replace('\n', '')
    return C1, C2, C3
# Get Labels--------------------------------
def get_labels(soup):
    lase = soup.find_all('div', class_ = 'content__labels')
    if lase == []:
        labelsers = ''
        labelsecs = ''
    else:
        lase_bf = BeautifulSoup(str(lase[0]), 'html.parser')
        labelser = lase_bf.find_all('div', class_ = 'content__series-label')
        labelsec = lase_bf.find_all('div', class_ = 'content__section-label')

        if labelser == []:
            labelsers = ''
        else:
            labelsers = labelser[0].get_text().replace('\n', '')
                        

        if labelsec == []:
            labelsecs = ''
        else:
            labelsecs = labelsec[0].get_text().replace('\n', '')
    return labelsers, labelsecs
# Get Authors --------------------------------
def get_authors(soup):
    auth = soup.find_all('p', class_ = 'byline')
    authors = ['', '', '', '']
    if auth == []:
        authors = ['', '', '', '']
    else:
        auth_bf = BeautifulSoup(str(auth[0]), 'html.parser')
        author = auth_bf.find_all('span', itemprop = 'name')
                
        if author == []:
            authors = ['', '', '', '']
        else:
            if len(author) == 1: # if there is only 1 author
                authors[0] = author[0].get_text()
                authors[1] = ''
                authors[2] = ''
                authors[3] = ''
            elif len(author) == 2: # if there are 2 authors
                authors[0] = author[0].get_text()
                authors[1] = author[1].get_text()
                authors[2] = ''
                authors[3] = ''
            elif len(author) == 3: # if there are 3 authors
                authors[0] = author[0].get_text()
                authors[1] = author[1].get_text()
                authors[2] = author[2].get_text()
                authors[3] = ''
            elif len(author) == 4: # if there are 4 authors
                authors[0] = author[0].get_text()
                authors[1] = author[1].get_text()
                authors[2] = author[2].get_text()
                authors[3] = author[3].get_text()
            else: # if there are more than 4 authors
                authors[0] = author[0].get_text()
                authors[1] = author[1].get_text()
                authors[2] = author[2].get_text()
                authors[3] = author[3].get_text()
    return authors
# Get Publish Time------------------------------
def get_time(soup):
    tim = soup.find_all('p', class_ = 'content__dateline')
    if tim == []:
        times = ''
    else:
        tim_bf = BeautifulSoup(str(tim[0]), 'html.parser')
        time = tim_bf.find_all('time', itemprop = 'datePublished')
        if time == []:
            times = ''
        else:
            times = time[0].get('datetime')
    return times
# Get News Description------------------------------
def get_description(soup):
    des = soup.find_all('div', class_ = 'content__standfirst')
    if des == []:
        descris = ''
    else:
        des_bf = BeautifulSoup(str(des[0]), 'html.parser')
        descri = des_bf.find_all('meta', itemprop='description')
        if descri == []:
            descris = ''
        else:
            descris = descri[0].get('content')
    return descris
# Get News Content------------------------------
def get_content(soup):
    con = soup.find_all('div', itemprop="articleBody")
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
    
    for i in range(27, 50): # from page 1 to 10
        target = 'https://www.theguardian.com/world/coronavirus-outbreak?page={}'.format(i)
        req = requests.get(url = target)
        html = req.text
        div_bf = BeautifulSoup(html, 'html.parser')
        div = div_bf.find_all('div', class_ = 'fc-container__body')
        a_bf = BeautifulSoup(str(div[0]), 'html.parser')
        a = a_bf.find_all('a', 'u-faux-block-link__overlay')

        for each in a:
            try:
                titles = each.get_text()
                urls = each.get('href')
            
                target0 = each.get('href')
                req0 = requests.get(url = target0)
                html0 = req0.text
                div_bf0 = BeautifulSoup(html0, 'html.parser')

                keyresult = get_keywords(soup = div_bf0)#keyresult是一个有10个值的列表
                cateresult = get_categories(soup = div_bf0)#cateresult是一个元组
                labelresult = get_labels(soup = div_bf0)
                authresult = get_authors(soup = div_bf0)
                timeresult = get_time(soup = div_bf0)
                desresult = get_description(soup = div_bf0)
                conresult = get_content(soup = div_bf0) 
                sql = "INSERT INTO theguarnews (Titles, Urls, Keyword1, Keyword2, Keyword3, Keyword4, Keyword5, Keyword6, Keyword7, Keyword8, Keyword9, Keyword10, C1, C2, C3, Labelsers, Labelsecs, Author1, Author2, Author3, Author4, Time, Description, Content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (titles, urls, keyresult[0], keyresult[1], keyresult[2], keyresult[3], keyresult[4], keyresult[5], keyresult[6], keyresult[7], keyresult[8], keyresult[9], cateresult[0], cateresult[1], cateresult[2], labelresult[0], labelresult[1], authresult[0], authresult[1], authresult[2], authresult[3], timeresult, desresult, conresult)
                mycursor.execute(sql, val)        
                mydb.commit()
            except IndexError:
                pass

# Main function----------------------------------------------
                
if __name__ == '__main__':
    #create table
    #sql = "CREATE TABLE theguarnews(id INT AUTO_INCREMENT PRIMARY KEY, Titles VARCHAR(255), Urls VARCHAR(255), Keyword1 VARCHAR(50), Keyword2 VARCHAR(50), Keyword3 VARCHAR(50), Keyword4 VARCHAR(50), Keyword5 VARCHAR(50), Keyword6 VARCHAR(50), Keyword7 VARCHAR(50), Keyword8 VARCHAR(50), Keyword9 VARCHAR(50), Keyword10 VARCHAR(50), C1 VARCHAR(50), C2 VARCHAR(50), C3 VARCHAR(50), Labelsers VARCHAR(50), Labelsecs VARCHAR(50), Author1 VARCHAR(50), Author2 VARCHAR(50), Author3 VARCHAR(50), Author4 VARCHAR(50), Time VARCHAR(50), Description VARCHAR(700), Content VARCHAR(10000))"
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
        
mycursor.execute("SELECT * FROM theguarnews")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)

'''
'''
#Export as excel file
import xlwt
import mysql.connector

row0 = ['Titles', 'Urls', 'Keyword1', 'Keyword2', 'Keyword3', 'Keyword4', 'Keyword5', 'Keyword6', 'Keyword7', 'Keyword8', 'Keyword9', 'Keyword10', 'C1', 'C2', 'C3', 'Labelsers', 'Labelsecs', 'Author1', 'Author2', 'Author3', 'Author4', 'Time', 'Description', 'Content']
book = xlwt.Workbook(encoding='utf-8')

#获取MYSQL中theguarnews表格中的所有数据
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="wsgtcdddtc",
    database="mydatabase"
    )
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM theguarnews")
myresult = mycursor.fetchall()

#获取MYSQL里面的数据字段名称
fields = mycursor.description

#注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
#cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
sheet = book.add_sheet('March3', cell_overwrite_ok=True)
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

book.save("theguarnews.xls")#给表格命名并保存，这个时候“下载”文件夹中就会多出一个excel文件了～
'''

#清空表格内容
#sql = "TRUNCATE TABLE theguarnews"
#mycursor.execute(sql)
#mydb.commit()
#mycursor.execute("TRUNCATE TABLE theguarnews")

#删除表格
#sql = "DROP TABLE theguarnews"
#mycursor.execute(sql)


#连接数据库
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="wsgtcdddtc",
    database="mydatabase"
    )
mycursor = mydb.cursor()
mycursor.execute("TRUNCATE TABLE theguarnews")
mydb.commit()
#mycursor.execute("alter table theguarnews change Content Content varchar(10000) character set utf8mb4")
'''
