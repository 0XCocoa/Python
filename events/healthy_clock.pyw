import tkinter
from time import sleep
from pathlib import Path
import tkinter.messagebox
from retrying import retry
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

sleep(3)

error_report = []
now = str(datetime.now()).split(' ')[0]
target_path = Path('D:\Tools\VS Code\Python\__pycache__\day.txt')


def whether():
    global now
    now_time = float(str(datetime.now()).split(' ')[1].replace(':','.')[:5])
    if not 5 <= now_time <= 19.3:
        return
    with open(target_path,'r',encoding='utf-8') as f:
        texts = f.read().strip().split('\n')
    if now != texts[0] or texts[1] == 'not yet':
        return True

@retry(stop_max_attempt_number=3,wait_fixed=600)
def click(x,by_type):
    driver.find_element(by_type, x).click()

def clicks(path_list=[],by_type=By.XPATH):
    if type(path_list) == str:
        path_list = [path_list]
    for x in path_list:
        click(x,by_type)

# 物理点击
def clicks_2(Xpath=[],Css=[]):
    clicks(Xpath)
    if type(Xpath) == str:
        temp = [Css]
        Css = temp
    for i,j in zip(Xpath,Css):
        clicks(i)
        item = driver.find_element(By.CSS_SELECTOR,j)
        ActionChains(driver).click(item).perform()
        sleep(0.5)

def scroll(driver):
	h = 0
	while h != driver.find_element_by_tag_name('body').size.get('height'):
		driver.execute_script('window.scroll(0, arguments[0])', h)
		sleep(1)
		h = driver.find_element_by_tag_name('body').size.get('height')

# 获取信息以确认是否需要
def if_next(Xpath,word='请选择'):
    txt = driver.find_element(By.XPATH,Xpath).text
    if txt == word:
        return True

def main():
    # 打开并登录厦大
    href = 'https://xmuxg.xmu.edu.cn/app/214'
    driver.get(href)
    clicks(['/html/body/div[1]/div/div[3]/div[2]/div/button[3]'])
    driver.find_element(By.ID,"username").send_keys(34520212201667)
    driver.find_element(By.ID,"password").send_keys('Abmlhyst1314')
    clicks(['/html/body/div[3]/div[2]/div[2]/div/div[3]/div/form/p[4]/button'])

    # 打开健康填报系统
    driver.get(href)
    clicks(['/html/body/div[1]/div/div/div/div/div[1]/div[2]/div/div[3]/div[2]'])
    sleep(1)
    
    # 在校状况
    if if_next('//*[@id="select_1611108284522"]/div/div/span[1]'):
        clicks_2(['/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[14]/div/div/div', 
                '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[17]/div/div/div', 
                '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[18]/div/div/div', 
                '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[19]/div/div/div', 
                '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[20]/div/div/div'], 
                ['body > div.v-select-cover > ul > div > div.gm-scroll-view > li:nth-child(1)', 
                'body > div.v-select-cover > ul > div > div.gm-scroll-view > li:nth-child(2)', 
                'body > div.v-select-cover > ul > div > div.gm-scroll-view > li:nth-child(1)', 
                'body > div.v-select-cover > ul > div > div.gm-scroll-view > li:nth-child(1)', 
                'body > div.v-select-cover > ul > div.v-gm-scrollbar.items-group.top.gm-autoshow.gm-scrollbar-container > div.gm-scroll-view > li:nth-child(180)'])
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[21]/div[1]/input').send_keys('0412')

    if if_next('//*[@id="datetime_1660308822369"]/div/div','请选择日期'):
        try:
            clicks(['/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[31]/div/div/div',
                    '/html/body/div[8]/div[1]/div/div/div[3]/span[11]'])
        except:
            pass

    # 填报
    if if_next('//*[@id="select_1582538939790"]/div/div/span[1]'):

        clicks_2('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[34]/div/div/div', 'body > div.v-select-cover > ul > div > div.gm-scroll-view > li')
        

        # 保存并关闭
        clicks(['/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/span/span'])
        try:
            driver.switch_to.alert.accept()
            sleep(1)
            driver.find_element_by_xpath("//*[text()='保存成功']")
            global now
            with open(target_path,'w',encoding='utf-8') as f:
                f.write(f'{now}\nalready\n')

        # error反馈：写入
        except:
            global error_report
            error_report.append('乾峰')
    else:
        with open(target_path,'w',encoding='utf-8') as f:
            f.write(f'{now}\nalready\n')

    driver.quit()

# 结果反馈
def show():
    global error_report
    if not error_report:
        tkinter.Tk().withdraw()
        tkinter.messagebox.showinfo('','already')
    else:
        tkinter.Tk().withdraw()
        tkinter.messagebox.showerror('未正常打卡，请手动打卡并检查问题',error_report)

# 独立运行检测
if __name__ == '__main__':
    if whether():
        driver = webdriver.Edge(executable_path=r"D:\Tools\VS Code\others\Microsoft Edge Driver\msedgedriver.exe")
        res = main()
    show()
