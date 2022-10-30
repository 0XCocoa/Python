import parsel
import requests
import pyautogui
from tqdm import tqdm
from time import sleep
 

def get_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47',
        # 防止连接数过多
        'Connection': 'close'
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding  # 自动转码
        return response
    except:
        # 连接超时
        raise ConnectionError(f'\n\nurl: {url} get failed...\n')

def str_find(item: list, txt: str)  -> bool:
    for x in item:
        if x in txt:
            return True

def upper(txt):
    try:
        txt = str(int(txt))
    except:
        return txt.replace('〇', '零')

    value = {'1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七','8':'八','9':'九','0':'零'}
    unit = ['个','十','百','千','万']
    
    txt = [(value[x] + unit[i] if i else value[x]) if x != '0' else '' for i,x in enumerate(reversed(txt))]
    print(txt)

    res = ''
    zero = 0
    for x in reversed(txt):
        if x:
            res += '零' + x if zero else x
            zero = 0
        else:
            zero = 1
    
    return res

def get_one_chapter(url):
    response = get_response(url)

    # 转行成selector解析对象
    selector = parsel.Selector(response.text)
    title = str(selector.css('.bookname h1::text').get()).strip()
    content = selector.css('#content::text').getall()

    # 格式化
    content = [x for x in content if x != '\n' and not str_find([title, title.split(' ')[0], f'《{novel_name}》','温馨提示'], x)]
    content = '\n'.join(content).replace('\r','').replace('\xa0',' ').replace('(本章未完！)\n\n    ','')
    title = '第' + upper(title[title.find('第')+1:title.find('章')]) + title[title.find('章'):]

    return title, content
 
def save(save_path, title, content):
    with open(save_path, mode='a', encoding='utf-8') as f:
        f.write(f'{title}\n\n{content}\n\n')
 
def get_all_url(url):
    response = get_response(url)

    # 转行成selector解析对象
    selector = parsel.Selector(response.text)
    novel_name = selector.css('#info h1::text').get()
    root = url[:url.find('.com/',0,-2)+4]
    paths = [(root + path) for path in selector.css('#list dd a::attr(href)').getall()]

    return novel_name, paths


if __name__ == '__main__':
    novel_name, paths = get_all_url('https://www.mayiwxw.com/65_65564/')
    save_path = f'D:/Files/下载/{novel_name}.txt'
    print(f'novel_name: {novel_name}\npart of paths: {paths[:4]}...')
    input()

    start = 0
    for path in (paths := tqdm(paths)):
        sleep(0.5)
        res = get_one_chapter(path)
        paths.set_description(f"Processing: {res[0]}")
        if start or (start := ('第一章' in res[0])):
            save(save_path, *res)

    pyautogui.alert(text='Finished...', title=f'《{novel_name}》')
