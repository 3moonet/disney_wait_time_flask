from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import datetime
from time import sleep

# driver_path = '.\main\chromedriver.exe' in local
driver_path = '/app/.chromedriver/bin/chromedriver'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"')

# park = "tdl" or "tds" must be str-type

# timely -----------------------
def get_wait_time(park):
    while True:
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

        url = f'https://www.tokyodisneyresort.jp/{park}/realtime/attraction/'
        driver.get(url)
        element = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located) # wait all elements

        # attraction data container
        a_datas = driver.find_elements_by_class_name('listItem')
        if len(a_datas) == 0:
            driver.quit()
            sleep(60)
            continue
        else:
            break

    d_list = []
    for a_data in a_datas:
        # attraction name
        name = a_data.find_element_by_tag_name('h3').text

        # wait time
        if len(a_data.find_elements_by_class_name('time')) > 0:
            time = a_data.find_element_by_class_name('time').text
        else:
            time = ''
        
        # fp(sp) time
        if len(a_data.find_elements_by_class_name('fastpassTime')) > 0:
            f_time = a_data.find_element_by_class_name('fastpassTime').text
        else:
            f_time = ''
        
        # tag(0=none, 1=fp(sp), 2=entry)
        tag_num=0
        if len(a_data.find_elements_by_class_name('iconTag')) > 0:
            tag_name = a_data.find_element_by_class_name('iconTag').text
            if tag_name=='スタンバイパス対象':
                tag_num = 1
            elif tag_name=='エントリー受付対象':
                tag_num = 2
            elif tag_name=='ファストパス対象':
                tag_num = 3
        
        d = {'name':name,'wait_time':time,'pass_time':f_time,'tag_id':tag_num}
        d_list.append(d)
            
    driver.quit()
    return d_list


# daily ---------------------------
def get_show_list(park): # realtimeなので営業時間中しか取得できない
    while True:
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

        url = f'https://www.tokyodisneyresort.jp/{park}/realtime/show/'
        driver.get(url)
        element = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located) # wait all elements

        shows = driver.find_elements_by_class_name('listItem')
        if len(shows) == 0:
            driver.quit()
            sleep(60)
            continue
        else:
            break

    show_list = []
    for show in shows:
        ng_word = '運営・公演中止'
        if ng_word not in show.find_element_by_class_name('timeTable2').text:
            name = show.find_element_by_class_name('heading3').text
            time = show.find_element_by_class_name('timeTable2').text
            show_list.append({'name':name, 'time':time})

    driver.quit()
    return show_list


# daily -------- 日付を確認する処理を追加 違うならやり直す
def get_opening_time(park):
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    today = datetime.datetime.now()
    today_num = today.strftime('%Y%m%d')

    url = f'https://www.tokyodisneyresort.jp/{park}/daily/calendar/{today_num}/'
    driver.get(url)
    element = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located) # wait all elements

    opening_time = driver.find_element_by_class_name('time').text
    driver.quit()
    return opening_time


def get_close_list_day(park):
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    today = datetime.datetime.now()
    today_num = today.strftime('%Y%m%d')

    url = f'https://www.tokyodisneyresort.jp/{park}/daily/stop/{today_num}/'
    driver.get(url)
    element = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located) # wait all elements

    sections = driver.find_elements_by_class_name('section')
    close_list_day=[]
    for section in sections:
        if len(section.find_elements_by_class_name('heading2')) > 0:
            if section.find_element_by_class_name('heading2').text=='アトラクション':
                for li in section.find_elements_by_tag_name('li'):
                    close_list_day.append(li.text)

    driver.quit()
    return close_list_day


# monthly ---------------------------
def get_close_list_month(park):
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    url = f'https://www.tokyodisneyresort.jp/{park}/monthly/stop/'
    driver.get(url)
    element = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located) # wait all elements

    blocks = driver.find_elements_by_class_name('accordionBlock')
    close_list_month=[]
    for block in blocks:
        if block.find_element_by_class_name('accordionTitle').text=='アトラクション':
            block.click()
            element = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located) # wait all elements

            for span in block.find_elements_by_tag_name('span'):
                name = span.find_element_by_tag_name('p').text
                date = span.find_element_by_class_name('date').text
                d = {'name':name, 'date':date}
                close_list_month.append(d)

    driver.quit()
    return close_list_month
