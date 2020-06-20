#引入相关模块
from bs4 import BeautifulSoup
import requests
'''
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="wsgtcdddtc",
  database="mydatabase"
)
mycursor = mydb.cursor()
'''

titles = []
urls = []
keywords1 = []
keywords2 = []
keywords3 = []
keywords4 = []
keywords5 = []
keywords6 = []
keywords7 = []
keywords8 = []
keywords9 = []
keywords10 = []
keywords = [keywords1, keywords2, keywords3, keywords4, keywords5, keywords6, keywords7, keywords8, keywords9, keywords10]
C1 = []
C2 = []
C3 = []
labelsers = []
labelsecs = []
authors1 = []
authors2 = []
authors3 = []
authors4 = []
times = []
descris = []
shares = []
comments = []


for i in range(2):
    target = 'https://www.theguardian.com/world/coronavirus-outbreak?page={}'.format(i + 1)
    req = requests.get(url = target)
    html = req.text
    div_bf = BeautifulSoup(html, 'html.parser')
    div = div_bf.find_all('div', class_ = 'fc-container__body')
    a_bf = BeautifulSoup(str(div[0]), 'html.parser')
    a = a_bf.find_all('a', 'u-faux-block-link__overlay')

    for each in a:
        try:
            titles.append(each.get_text())
            urls.append(each.get('href'))
            
            target0 = each.get('href')
            req0 = requests.get(url = target0)
            html0 = req0.text
            div_bf0 = BeautifulSoup(html0, 'html.parser')
            
            key = div_bf0.find_all('div', class_ = 'submeta__keywords')
            if key == []:
                keywords1.append("")
                keywords2.append("")
                keywords3.append("")
                keywords4.append("")
                keywords5.append("")
                keywords6.append("")
                keywords7.append("")
                keywords8.append("")
                keywords9.append("")
                keywords10.append("")
            else:
                key_bf = BeautifulSoup(str(key[0]), 'html.parser')
                keyword = key_bf.find_all('li', class_ = "submeta__link-item")
                keynum = len(keyword)
                if keynum < 10:
                    for i in range(0, keynum):
                        keywords[i].append(keyword[i].get_text().replace('\n', ''))
                    for i in range(keynum, 10):
                        keywords[i].append("")
                elif keynum >= 10:
                    for i in range(0, 10):
                        keywords[i].append(keyword[i].get_text().replace('\n', ''))
                    
            

            '''
            count = div_bf0.find_all('div', class_ = 'meta__numbers')
            if count == []:
                shares.append("")
                comments.append("")
            else:
                count_bf = BeautifulSoup(str(count[0]), 'html.parser')
                share = count_bf.find_all('div', class_ = "sharecount__value--full")
                if share == []:
                    shares.append("")
                else:
                    for x in share:
                        shares.append(x.get_text())
                comment = count_bf.find_all('span', class_ = "commentcount2__value")
                if comment == []:
                    comments.append("")
                else:
                    for x in comment:
                        comments.append(x.get_text())
            '''
            cate = div_bf0.find_all('header', class_ = 'new-header')
            if cate == []:
                C1.append("")
                C2.append("")
                C3.append("")
            else:
                cate_bf = BeautifulSoup(str(cate[0]), 'html.parser')
                c1 = cate_bf.find_all('a', class_ = "pillar-link--current-section")
                if c1 == []:
                    C1.append("")
                else:
                    for x in c1:
                        C1.append(x.get_text().replace('\n', ''))
                c2 = cate_bf.find_all('li', class_ = "subnav__item--parent")
                if c2 == []:
                    C2.append("")
                else:
                    for x in c2:
                        C2.append(x.get_text().replace('\n', ''))
                c3 = cate_bf.find_all('a', class_ = "subnav-link--current-section")
                if c3 == []:
                    C3.append("")
                else:
                    for x in c3:
                        C3.append(x.get_text().replace('\n', ''))

            
            lase = div_bf0.find_all('div', class_ = 'content__labels')
            if lase == []:
                labelsers.append("")
                labelsecs.append("")
            else:
                lase_bf = BeautifulSoup(str(lase[0]), 'html.parser')
                labelser = lase_bf.find_all('div', class_ = "content__series-label")
                labelsec = lase_bf.find_all('div', class_ = "content__section-label")
                if labelser is None:
                    labelsers.append("")
                elif labelser == []:
                    labelsers.append("")
                else:
                    for x in labelser:
                        labelsers.append(x.get_text().replace('\n', ''))
                        
                if labelsec is None:
                    labelsecs.append("")
                elif labelsec == []:
                    labelsecs.append("")
                else:
                    for x in labelsec:
                        labelsecs.append(x.get_text().replace('\n', ''))
            
               
            auth = div_bf0.find_all('p', class_ = 'byline')
            auth_bf = BeautifulSoup(str(auth[0]), 'html.parser')
            author = auth_bf.find_all('span', itemprop = "name")
            
            if author is None:
                authors1.append("")
                authors2.append("")
            else:
                authcon = []
                for x in author:
                    authcon.append(x.get_text())
                if len(authcon) == 0:
                    authors1.append("")
                    authors2.append("")
                    authors3.append("")
                    authors4.append("")
                elif len(authcon) == 1:
                    authors1.append(authcon[0])
                    authors2.append("")
                    authors3.append("")
                    authors4.append("")
                elif len(authcon) == 2:
                    authors1.append(authcon[0])
                    authors2.append(authcon[1])
                    authors3.append("")
                    authors4.append("")
                elif len(authcon) == 3:
                    authors1.append(authcon[0])
                    authors2.append(authcon[1])
                    authors3.append(authcon[2])
                    authors4.append("")
                elif len(authcon) == 4:
                    authors1.append(authcon[0])
                    authors2.append(authcon[1])
                    authors3.append(authcon[2])
                    authors4.append(authcon[3])
                else:
                    authors1.append(authcon[0])
                    authors2.append(authcon[1])
                    authors3.append(authcon[2])
                    authors4.append(authcon[3])
         
            tim = div_bf0.find_all('p', class_ = 'content__dateline')
            tim_bf = BeautifulSoup(str(tim[0]), 'html.parser')
            time = tim_bf.find_all('time', itemprop = "datePublished")
            if time is None:
                times.append("")
            else:
                for x in time:
                    times.append(x.get('datetime'))
            
            des = div_bf0.find_all('div', class_ = 'content__standfirst')
            des_bf = BeautifulSoup(str(des[0]), 'html.parser')
            descri = des_bf.find_all('meta', itemprop="description")
            if descri is None:
                descris.append("")
            else:
                for x in descri:
                    descris.append(x.get('content'))
            
            
            
        except IndexError:
             pass
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
#导出为excel文件
import xlwt
row0 = ['Titles', 'Urls', 'Labelsers', 'Labelsecs', 'Author1', 'Author2', 'Author3', 'Author4', 'Time', 'Description']
book = xlwt.Workbook(encoding='utf-8')

#获取MYSQL中theguarnews表格中的所有数据
mycursor.execute("SELECT * FROM theguarnews")
myresult = mycursor.fetchall()

#获取MYSQL里面的数据字段名称
fields = mycursor.description

#注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
#cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
sheet = book.add_sheet('卫报数据', cell_overwrite_ok=True)
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

book.save("卫报数据.xls")#给表格命名并保存，这个时候“下载”文件夹中就会多出一个excel文件了～

'''
#清空表格内容
#sql = "TRUNCATE TABLE theguarnews"
#mycursor.execute(sql)
#mydb.commit()
