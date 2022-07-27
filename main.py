from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

### TODO delete!
login_id = 'ID넣기'
login_pw = 'PW넣기'

lifecase_url = 'https://lge.lglifecare.com/search?displayCategoryNos=2574678,2574837,2574847,2574850&displayCategoryDepth=4&displayCategoryName=%EB%AA%A8%EB%8B%88%ED%84%B0&categoryKeyword=%2a&changeCategory=true'

driver = wb.Chrome()
driver.get(lifecase_url)
time.sleep(2)

id_text = driver.find_element(By.CSS_SELECTOR, value='#id')
wb.ActionChains(driver).send_keys_to_element(id_text, login_id).perform()

pw_text = driver.find_element(By.XPATH, value='//*[@id="__layout"]/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/input[2]')
wb.ActionChains(driver).send_keys_to_element(pw_text, login_pw).send_keys(Keys.ENTER).perform()
time.sleep(2)

# --> New session

new_url = 'https://lge.lglifecare.com/search?displayCategoryNos=2574678,2574837,2574847,2574850&displayCategoryDepth=4&displayCategoryName=%EB%AA%A8%EB%8B%88%ED%84%B0&categoryKeyword=%2a&changeCategory=true'
driver.get(new_url)
time.sleep(2)
html = driver.page_source
soup = bs(html, 'lxml')
info_list = soup.find_all(class_='item_cpn ga-prd')
print("Total item :", len(info_list))
title_list = []
price_list = []
link_list = []
for idx, ele in enumerate(info_list,1):
    if 'SOLD OUT' in ele.text:
        title_list.append((ele.find(class_='tit_cpn tit_cpn ga-prd-click').text).replace("등급모니터","sold out"))
    else:
        title_list.append(ele.find(class_='tit_cpn tit_cpn ga-prd-click').text)
    price_list.append(int((ele.find(class_='discount_cpn').text).replace(",","").replace(" 원","")))
    link_list.append("https://lge.lglifecare.com/" + ele.find("a")["href"])

item_dic = {
    "상품명" : title_list,
    "가격" : price_list,
    "링크" : link_list
}

item_df = pd.DataFrame(item_dic)
print(item_df.sort_values(by=['가격']))
