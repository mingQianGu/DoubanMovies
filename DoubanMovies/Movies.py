import urllib.request
from bs4 import BeautifulSoup
from time import strftime
import codecs
import re
import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from PIL import Image


def find_file(f_folder):  # 寻找文件夹下所有的文件，并汇聚成列表
    files = os.listdir(f_folder)
    filelist = []
    for file in files:
        filelist.append(f_folder + "//" + file)
    return filelist


def to_163(from_account, to_account, password_from):  # 使用163邮箱发送邮件
    m_host = 'smtp.163.com'
    m_port = 25
    m_from = from_account
    m_to = to_account
    m_subject = 'new_movie ' + strftime("%Y_%m_%d")  # 邮件标题
    m_content = '豆瓣新片榜:' + '\n\n'

    smtp_obj = smtplib.SMTP(m_host, m_port)  # 普通传输
    res = smtp_obj.login(user=m_from, password=password_from)
    print("登录成功")

    # 正文编辑
    msg = MIMEMultipart()
    msg['from'] = m_from
    msg['to'] = m_to
    msg['subject'] = m_subject
    m_txt = codecs.open('new_movie' + '//' + strftime("%Y_%m_%d") + '//' +
                        'new_movie' + strftime("%Y_%m_%d") + '.txt', 'r', 'utf-8')
    for line in m_txt.readlines():
        m_content += line
    txt = MIMEText(m_content, 'plain', 'utf-8')
    msg.attach(txt)

    # 附件
    folder = 'new_movie' + "//" + "pictures"
    filenames = find_file(folder)
    for file in filenames:
        if file == folder + "//" + strftime("%Y_%m_%d") + ".jpg":
            part = MIMEApplication(open(file, 'rb').read())
            part.add_header('Content-Disposition', 'attach', filename=file)
            msg.attach(part)

    smtp_obj.sendmail(from_addr=m_from, to_addrs=m_to, msg=msg.as_string())
    print("传输成功")


def douban(m_url, m_headers, m_infofile):  # 爬取豆瓣新片榜
    # 发送请求
    page = urllib.request.Request(m_url, headers=m_headers)
    page = urllib.request.urlopen(page)
    contents = page.read()
    # 用BeautifulSoup解析网页
    soup = BeautifulSoup(contents, "html.parser")
    # print(soup)
    m_infofile.write("")
    print('豆瓣新片榜: \n')
    count = 1
    pic_output = Image.new('RGB', (270, 4000), 'white')

    if os.path.exists('new_movie' + "//" + "pictures"):
        pass
    else:
        os.mkdir('new_movie' + "//" + "pictures")
    if os.path.exists('new_movie' + "//" + strftime("%Y_%m_%d")):
        pass
    else:
        os.mkdir('new_movie' + "//" + strftime("%Y_%m_%d"))

    for tag in soup.find_all(attrs={"class": "item"}):
        print("#" + str(count))
        count += 1
        # 电影名称
        a_attrs = tag.a.attrs
        chinese_name = a_attrs.get("title")
        print('[中文名称]', chinese_name)
        m_infofile.write("[中文名称]" + chinese_name + "\r\n")
        # 电影图片
        url_img_attrs = tag.img.attrs
        url_img = url_img_attrs.get("src")
        name_img = "new_movie" + "//" + strftime("%Y_%m_%d") + "//" + chinese_name + ".jpg"
        if os.path.exists(name_img):
            pass
        else:
            image = requests.get(url_img).content
            with open(name_img, 'wb') as f:
                f.write(image)
        img = Image.open("new_movie" + "//" + strftime("%Y_%m_%d") + "//" + chinese_name + ".jpg")
        img_s = img.resize((270, 400), Image.NEAREST)
        pic_output.paste(img_s, (0, 400 * (count - 2)))
        # print(url_img)
        # 上映时间
        a_time = tag.find(attrs={"class": "pl"}).get_text()
        time = re.match('(.*?)(/)(.*)', a_time)
        print('[上映时间]', time.group(1))
        m_infofile.write("[上映时间]" + time.group(1) + "\r\n")
        # 网页链接
        url_movie = a_attrs.get("href")
        print('[网页链接]', url_movie)
        m_infofile.write("[网页链接]" + url_movie + "\r\n")
        # 爬取评分和评论数
        rate = tag.find(attrs={"class": "rating_nums"}).get_text()
        a_num = tag.find_all(attrs={"class": "pl"})
        num = a_num[1].get_text()
        print('[最新评分]', rate + num)
        m_infofile.write("[最新评分]" + rate + num + "\r\n" + "\r\n")
    pic_output.save('new_movie' + "//" + "pictures" + "//" + strftime("%Y_%m_%d") + ".jpg")
