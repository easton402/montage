#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @文件名(file): autoswoa.py
# @作者(author): uchen
# @邮箱(mail): zjax-005@163.com
# @时间(date): 2013-01-05

import urllib2
import urllib
import cookielib
import json
import datetime
import time

class Login_Oa():
    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(self.opener)
        self.opener.addheaders = [("User-agent", "Mozilla/4.0 (compatible); MSIE 6.0; Windows NT 5.1")]

    def login(self, username, password):
        url = "http://oa.shunwang.com/doLogin.do"         ## 可换成你想登录站点的url
        data = {"username":username,"password":password}  ##登陆用户名和密码
        post_data = urllib.urlencode(data)
        req = urllib2.Request(url, post_data)
        try:
            content = self.opener.open(req)
        except Exception, e:
            print(u'网络连接错误！')
            return False
        login_js = json.loads(content.read())    ##返回字符串
        if login_js["result"] != "success":
            print u"用户名密码不匹配！"
            return False
        else:
            print u"%s 登陆成功！" % (username)
        return True

    def logout(self):
        url = "http://oa.shunwang.com/loginout.do"        ## 可换成你想退出站点的url
        req = urllib2.Request(url)
        html = self.opener.open(req)
        html.close()

    def checkpunch(self):
        current_unix_time = repr(time.time()*1000).split('.')[0]   ##获取当前unix时间戳并转换成str
        today = datetime.date.today()
        curr_year = today.strftime('%Y')
        curr_month = today.strftime('%m')
        yesterday = today - datetime.timedelta(days=1)
        two_days_ago = today - datetime.timedelta(days=2)
        three_days_ago = today - datetime.timedelta(days=3)
        check_date = []
        date_list = [yesterday.strftime('%Y-%m-%d'), two_days_ago.strftime('%Y-%m-%d'), three_days_ago.strftime('%Y-%m-%d')]
        for item in date_list:     ##将日志加上" 00:00:00"
            check_date.append(item + " 00:00:00")
        
        url = "http://oa.shunwang.com/front/attendance/month.do?year="+ curr_year + "&month=" + curr_month + "&_=" + current_unix_time  ##查询当前年、月的考勤的url
        req = urllib2.Request(url)
        html = self.opener.open(req)
        checkpunch_js = json.loads(html.read())
        valid_date = [item for item in check_date if item in checkpunch_js.keys()]   ##取得两个列表的交集        
        for query_date in valid_date:        
            print u"------------华丽丽的分割线------------"
            print u"考勤日期: %s %s \n考勤人: %s\n考勤状态: %s\n\n第一次打卡时间: %d:%d\n早上打卡时间: %d:%d\n最后一次打卡时间: %d:%d\n下午打卡时间: %d:%d\n" % (query_date.split()[0],\
                                           checkpunch_js[query_date]["record"]["recordweekday"],\
                                           checkpunch_js[query_date]["record"]["realName"],\
                                           checkpunch_js[query_date]["record"]["attendanceStatus"],\
                                           checkpunch_js[query_date]["record"]["firstPunch"]["hours"],\
                                           checkpunch_js[query_date]["record"]["firstPunch"]["minutes"],\
                                           checkpunch_js[query_date]["record"]["morningPunch"]["hours"],\
                                           checkpunch_js[query_date]["record"]["morningPunch"]["minutes"],\
                                           checkpunch_js[query_date]["record"]["lastPunch"]["hours"],\
                                           checkpunch_js[query_date]["record"]["lastPunch"]["minutes"],\
                                           checkpunch_js[query_date]["record"]["afternoonPunch"]["hours"],\
                                           checkpunch_js[query_date]["record"]["afternoonPunch"]["minutes"])
        html.close()
           
if __name__ == '__main__':
    l = Login_Oa()
    name = 'username'     ## 这里修改登录用户名
    passwd = 'password'   ## 这里修改登录密码
    if l.login(name, passwd) == False:
        exit(1)
    l.checkpunch()


