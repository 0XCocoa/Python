from time import sleep
from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Webdriver:
    def __init__(self, eager=None):
        path = r"D:\Tools\VS Code\others\Microsoft Edge Driver\msedgedriver.exe"
        if not eager:
            driver = webdriver.Edge(executable_path=path)
        else:
            #get直接返回，不再等待界面加载完成
            capabilities = DesiredCapabilities.EDGE
            capabilities["pageLoadStrategy"] = "eager"
            driver = webdriver.Edge(executable_path=path, capabilities = capabilities)
    
        self.driver = driver
    
    @retry(stop_max_attempt_number=3,wait_fixed=600)
    def click(self, i):
        self.driver.find_element(By.XPATH, i).click()

    def clicks(self, path_list=[]):
        if isinstance(path_list,str):
            path_list = [path_list]
        for i in path_list:
            self.click(i)

    def if_active(self, path, click=True):
        button = self.driver.find_element(By.XPATH, path)
        if button.is_enabled():
            if click:
                button.click()
            return True
        else:
            return False
    
    def scroll(self):
        driver = self.driver
        h = 0
        while h != driver.find_element_by_tag_name('body').size.get('height'):
            driver.execute_script('window.scroll(0, arguments[0])', h)
            sleep(1)
            h = driver.find_element_by_tag_name('body').size.get('height')