
from turtle import title
import requests
from bs4 import BeautifulSoup
import pandas as pd

element="Gold"
element=element.lower().replace(" ","_")
print(element)
url='https://oilprice.com/search/tab/articles/'+element
html=requests.get(url).content
soup=BeautifulSoup(html,"html.parser")
df=pd.DataFrame(columns=['Date','Title'	,'Articles'])
content=soup.find('div', attrs={"class":"search-results"}).find_all('a', href=True)
print(content)
for i in content:
    title=i.text
    link=i.get('href')
    html=requests.get(link).content
    s=BeautifulSoup(html,"html.parser")
    content=s.find('div', attrs={"id":"article-content"}).text.strip()
    date=s.find('span', attrs={"class":"article_byline"}).text
    #By Felicity Bradstock - Oct 07, 2022, 5:00 PM CDT
    date=date.split('-')[1].strip()[:-3].replace(',','')
    df.loc[len(df)]=[date,title,content]
print(df.to_csv(f"{element}.csv",index=False))


    