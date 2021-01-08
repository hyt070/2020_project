import xlwt
import re
import requests
from bs4 import BeautifulSoup
#找到网址
www = re.compile(r'href="//(.*?)" target="_blank">')
#找到名称
name = re.compile(r'target="_blank">(.*?)</a>')
#找到播放次数
play = re.compile(r'<i class="b-icon play"></i>(.*?)</span>',re.S)
#找到弹幕数量
view = re.compile(r'<i class="b-icon view"></i>(.*?)</span>',re.S)
#找到追番或追剧人数
fav = re.compile(r'<i class="fav"></i>(.*?)</span>',re.S)
#找到综合评分
toal = re.compile(r'<div class="pts"><div>(.*?)</div>')




def main():
    s=input("请输入你要爬取的哔哩哔哩排行榜：1.番剧 2.国产动画 3.纪录片 4.电影 other.电视剧\n")
    if s == '1':
        qer = "bangumi"
        pqe ="番剧"
    elif s == '2':
        qer = "guochan"
        pqe = "国产动画"
    elif s == '3':
        qer = "documentary"
        pqe = "纪录片"
    elif s == '4':
        qer = "movie"
        pqe = "电影"
    else:
        qer = "tv"
        pqe = "电视剧"

    #数据爬取
    html = requests.get(f"https://www.bilibili.com/v/popular/rank/{qer}").text
    datalist = []
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all('div',class_= "info"):
        data=[]
        item=str(item)
        link1 = re.findall(name,item)[0]
        link2 = re.findall(www,item)[0]
        link3 = re.findall(play, item)[0].replace('\n', '').replace('\r', '').strip()
        link4 = re.findall(view, item)[0].replace('\n', '').replace('\r', '').strip()
        link5 = re.findall(fav, item)[0].replace('\n', '').replace('\r', '').strip()
        link6 = re.findall(toal, item)[0]
        data.append(link1)
        data.append(link2)
        data.append(link3)
        data.append(link4)
        data.append(link5)
        data.append(link6)
        datalist.append(data)

    print(" 名称                                  网址                        播放次数       弹幕数量     追番或追剧人数     综合评分")
    for f in datalist:
        print(f)


    #数据保存
    book=xlwt.Workbook(encoding="utf-8")
    sheet=book.add_sheet(f"bilibili{pqe}排行榜")
    col=("名称","网址","播放次数","弹幕数量","追番或追剧人数","综合评分",)
    for i in range(0,6):
        sheet.write(0,i,col[i])
        f=1
    for x in datalist:
        for j in range(0,6):
            sheet.write(f,j,x[j])
        f+=1
    book.save("bilibili排行榜.xls")
    print("数据已存储在exl表中")




if __name__ == '__main__':
    main()