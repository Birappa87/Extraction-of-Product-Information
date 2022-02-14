import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time


base_url = "https://www.screwfix.com/c/tools/drills/cat830704#category=cat830704"

def getdata(url):
  headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}
  try:
    r = requests.get(url ,headers= headers)
    soup = BeautifulSoup(r.content, 'lxml')
  except:
    print("Request failed")
    time.sleep(5)
  
  return soup

#getting next page 
def get_next_page(soup):
  page = soup.find('div' ,class_ = 'pagi')
  if not page.find('a' ,attrs = {"class" :"btn btn--disabled pagi__link","id" :"next_page_link"}):
    total_page = page.find('label' , 'pagi__text pagi__page--total')
    print(total_page)
    url = page.find('a' , id = 'next_page_link') 
    page_url = url['href']
  else:
    return  

  return page_url

product_page_links = ["https://www.screwfix.com/c/tools/drills/cat830704#category=cat830704"] 
while True:
  home_page = getdata(base_url)
  next_page_link = get_next_page(home_page)
  base_url = next_page_link
  if base_url !=None:
    product_page_links.append(base_url)

  if not next_page_link:
    break
  else:
    continue

title_list = []
link_list = []
for link in product_page_links:
  page_data = getdata(link)
  product_body = page_data.find_all('div' ,class_= 'product-box')
  for elements in product_body:
    product_tag = elements.find('a')
    title = product_tag['title'].strip()
    title_list.append(title)
    link = product_tag['href'].strip()
    link_list.append(link)

data = {'Title' : title_list , 'Link' : link_list}
df = pd.DataFrame(data)
print(df.head())
df.to_csv('data.csv')

      

  


