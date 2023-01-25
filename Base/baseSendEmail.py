# encoding:utf-8

import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Base.BasePath import BasePath as BP
from Base.utils import read_config_ini, make_zip

class HandleEmail:
    def __init__(self):
        config = read_config_ini(BP.Config_File)['邮件发送配置']
        self.host = config['host']
        # 因为配置文件中都是字符串，所以通过int转为数字
        self.port = int(config['port'])
        # 发送方的名字，一般指测试人员
        self.sender = config['sender']
        # 发送方email
        self.send_email = config['send_email']
        # 接收方email 如果设置为列表格式，则为群发
        # 防止转换后依然还是字符串
        if isinstance(eval(config['receiver']), str):
            self.receiver = eval(eval(config['receiver']))
        else:
            self.receiver = eval(config['receiver'])
        # 授权码
        self.psw = config['pwd']
        # 主题 格式字符串
        self.subject = config['subject']

    # 在邮件中添加正文
    def add_text(self, text):
        return MIMEText(text, 'plain', 'utf-8')

    # 添加HTML代码
    def add_html_text(self, html):
        return MIMEText(html, 'html', 'utf-8')

    # 添加附件
    def add_accesory(self, filepath):
        res = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
        res.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
        return res

    # 添加邮件发送人，接收人，主体
    #  attach 附件
    def add_subject_attach(self, attach_info:tuple, send_date=None):
        msg = MIMEMultipart('mixed')
        # 设置邮件主题
        msg['Subject'] = self.subject
        # 设置发件人
        msg['From'] = '{} <{}>'.format(self.sender, self.send_email)
        # 设置收件人
        msg['To'] = ';'.join(self.receiver)
        # 判断send_data是否有值
        # 如果有，则按照设置的值
        # 如果没有，则获取当前时间
        if send_date:
            msg['Date'] = send_date
        else:
            msg['Date'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        # 判断附件是否为元组
        if isinstance(attach_info, tuple):
            # 循环添加附件
            for i in attach_info:
                msg.attach(i)
        return msg


    # 发送邮件
    # msg：要发送的内容
    def send_email_oper(self, msg):
        # 通过两种方式发送
        try:
            # 通过smtp发送
            # 创建smtp对象
            smtp = smtplib.SMTP(self.host, port=self.port)
            # 登录
            smtp.login(self.send_email, self.psw)
            # 发送邮件
            smtp.sendmail(self.send_email, self.receiver, msg.as_string())
            print('{}给{}发送邮件成功，发送时间：{}'.format(self.send_email, self.receiver,
                                               datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
        except Exception as e:
            # 通过SMTP_SSL发送
            # 创建smtp对象
            smtp = smtplib.SMTP_SSL(self.host, port=self.port)
            # 登录
            smtp.login(self.send_email, self.psw)
            # 发送邮件
            smtp.sendmail(self.send_email, self.receiver, msg.as_string())
            print('{}给{}发送邮件成功，发送时间：{}'.format(self.send_email, self.receiver,
                                               datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
        finally:
            smtp.quit()


    # 最终发送方法
    def send_public_email(self, send_date=None, text='', html='', filetpye='ALLURE'):
        '''邮件发送公共方法'''
        attach_info = []
        # 使用上面的新增文本方法
        text_plain = self.add_text(text=text)
        # 将文本添加到attach_info中
        attach_info.append(text_plain)
        # 判断html是否有值
        if html:
            # 如果有值，则添加到列表中
            text_html = self.add_html_text(html=html)
            attach_info.append(text_html)
        elif filetpye == 'ALLURE':
            # 如果测试报告为allure，则使用打包方法，创建成压缩文件
            allure_zip = make_zip(BP.Allure_Dir, os.path.join(BP.Allure_Dir, 'ALLURE.zip'))
            file_attach = self.add_accesory(filepath=allure_zip)
            attach_info.append(file_attach)
        elif filetpye == 'HTML':
            # 如果测试报告为HTML，则直接添加到列表中
            file_attach = self.add_accesory(filepath=os.path.join(BP.HTML_Dir, 'auto_reports.html'))
            attach_info.append(file_attach)
        elif filetpye == 'XML':
            # 如果测试报告为HTML，则直接添加到列表中
            file_attach = self.add_accesory(filepath=os.path.join(BP.XML_Dir, 'auto_reports.xml'))
            attach_info.append(file_attach)
        # 添加主题、附件等信息添加到msg中
        msg = self.add_subject_attach(attach_info=tuple(attach_info), send_date=send_date)
        # 通过上面的方法，发送邮件
        self.send_email_oper(msg)


if __name__ == '__main__':
    text = '测试'
    HandleEmail().send_public_email(text=text)




