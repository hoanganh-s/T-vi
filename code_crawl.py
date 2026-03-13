import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup
import random

base_url = 'https://tuvi.cohoc.net'
print('Starting Chrome...')

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


data = []

try:
    for page in range(624, 835):
        print(f'\n--- Scraping page {page} ---')
        page_url = f'{base_url}/hoc-tu-vi.html' if page == 1 else f'{base_url}/hoc-tu-vi-{page}.html'

        driver.get(page_url)
        print('Wait for page load...')
        time.sleep(4)
        
        elements_a = driver.find_elements(By.TAG_NAME, 'a')
        list_link = []

        for a in elements_a:
            href = a.get_attribute('href')
            if href and '-nid-' in href and href.endswith('.html'):
                if href not in list_link:
                    list_link.append(href)

        for index, url_block in enumerate(list_link):
            
            
            driver.get(url_block)

            rest_time = random.uniform(2,8)
            time.sleep(rest_time)

            
            try:
                title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
            except:
                title = 'No title'

            
            try:
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                content = soup.find('div', class_='noi-dung')

                if content is not None:
                    elements = content.find_all(['p', 'h2', 'li', 'h3'])
                    knowledge = [] 
                    
                    for element in elements:
                        text = element.text.strip()
                        if text != '':
                            
                            knowledge.append(text)
                    
                    
                    data.append({
                        "url": url_block,
                        "tittle": title,
                        "content": knowledge
                    })
                    print('  -> Successful!')
                else:
                    print('  -> Error')
                    
            except Exception as ex:
                print(f'  -> Sth wrong {ex}')

except Exception as e:
    print(f'Something wrong: {e}')

finally:
    driver.quit()


file_name = 'Hoc_tu_vi14.json'
with open(file_name, mode='w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
    