# -*- coding: UTF-8 -*-

import MySQLdb
import re #主要包含了正则表达式
import urllib #　Urllib 模块提供了读取web页面数据的接口

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getCountryInfo():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='000000', db='python',charset='utf8')
    cursor = conn.cursor()

    select = "select id, country_name, country_url from Country"
    try:
        cursor.execute(select)
        if cursor.rowcount == 0:
            
            sql_value = False
            # cursor.execute(select)

        else:
            sql_value = True
        
            # print sql_value

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e


    rs = cursor.fetchall()
    for country in rs:
        country_id = country[0]
        country_name = country[1]
        country_url = country[2]
        # print country_id; print country_url;

        urlStr = country_url + "citylist-1-0-1/"
        # print urlStr
        cityTotalUrl = getHtml(urlStr)
        getCity(cityTotalUrl)
        # insert_city_sql = 
    cursor.close();
    conn.close();
    
def getCity(html):

    reg = r'<a href="(//place.qyer.com/.*/)" target="_blank" data-bn-ipg="place-citylist-text-city-1">([\s\S]*?)&nbsp;&nbsp;<span class="en">([\s\S]*?)<\/span>'
    '''
    ([\s\S]*?) +<span class="en">([\s\S]*?)</span>'
    '''
    cityre = re.compile(reg)#re.compile(pattern[, flags])将reg转化成正则表达式对象
    citylist = re.findall(cityre,html)
    print citylist
    # for city in citylist:
    #     link = city[0];
    #     name = city[1];
    #     enname = city[2];
    #     print link; print name; print enname;



def getCountries(html):

    conn = MySQLdb.connect(host='localhost', user='root', passwd='000000', db='python',charset='utf8')
    cursor = conn.cursor()

    reg = r'<a href="(http://place.qyer.com/.*/)" data-bn-ipg="place-index-countrylist-\d+">\r\n +([\s\S]*?) \r\n +<span class="en">([\s\S]*?)<\/span>\r\n +<\/a>'

    countryre = re.compile(reg)#re.compile(pattern[, flags])将reg转化成正则表达式对象
    countrylist = re.findall(countryre,html)
    for country in countrylist:
        link = country[0];
        name = country[1];
        enname = country[2];

#        print link; print name; print enname;
        sql_select = "select * from Country where country_name = '%s'" % (name)

        sql_insert = "insert into Country(country_name,country_en, country_url) values('%s', '%s', '%s')" % (name, enname, link)
        try:
            cursor.execute(sql_select)
            if cursor.rowcount == 0:
            
                sql_value = False
                cursor.execute(sql_insert)

            else:
                sql_value = True
        
            # print sql_value

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

    cursor.close();
    conn.close();

# city = getHtml("http://place.qyer.com")
# getCountries(city)
getCountryInfo()


'''
<a href="//place.qyer.com/london/" target="_blank" data-bn-ipg="place-citylist-text-city-1">伦敦&nbsp;&nbsp;<span class="en">London</span></a></h3>
'''