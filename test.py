# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys

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
    print(type(a_bf), type(a), type(div_bf), type(div))
    print(a)

