import requests
import time
from bs4 import BeautifulSoup
import re
from google.colab import drive
import pandas as pd

def get_page_html(url, delay=2):
    time.sleep(delay)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на успешность запроса
        response.encoding = response.apparent_encoding or 'utf-8'
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None

def save_html_to_file(html_content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        # print(f"HTML сохранен в файл: {filename}") # Надо потом убрать
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

def filter_numeric_ranges(arr):
    pattern = re.compile(r'^\d+([-+]\d+)?\+?$')
    pattern2 = re.compile(r'^\d+([-+]\d+)?\+?$')
    return [item for item in arr if pattern2.match(item)]

def Dlya_Artema(arr):
    result = []
    for item in arr:
        parts = re.findall(r'[A-ZА-ЯЁ][^A-ZА-ЯЁ]*', item, re.UNICODE)
        if not parts:
            parts = [item]
        result.append(parts)
    return result

#Название
def make_name(a):
    imya = a.find_all(class_='product-card-title')[0]
    link = imya.find('a')
    title_value = link.get('title')
    return title_value

#Count_Gamers, Time, Age
def Count_Gamers_Time_Age(a):
    q = a.find_all(class_='product-card__tags')[0]
    b = q.find_all(class_='product-tag__label')
    values = [tag.get_text(strip=True) for tag in b]
    iform = filter_numeric_ranges(values)
    return iform

# Ищем ссылку на Котегории и Thematics
def find_link(a):
      ssilka = a.find_all(class_='product-card-title')[0]
      title_value = ssilka.find('a')
      title_value_a = title_value.get('href')
      link = "https://hobbygames.ru" + title_value_a
      return link

# Получаем Thematics и Categories
def Thematics_Categories(html_content_dob):
  soup_dob = BeautifulSoup(html_content_dob, 'html.parser')
  product_cards_dob = soup_dob.find_all(class_='tags')
  values_dob = [tag.get_text(strip=True) for tag in product_cards_dob]
  values_dob = values_dob[:len(values_dob) // 2]
  q = Dlya_Artema(values_dob)
  return q

def link_stranicy(g):
  url = f"https://hobbygames.ru/nastolnie?page={g}";
  html = get_page_html(url)
  if html:
    save_html_to_file(html, "boardgamegeek_page.html")
    print(f"Общий размер HTML: {len(html)} символов")
  else:
    print("Не удалось получить HTML-код страницы.")
  with open('boardgamegeek_page.html', 'r', encoding='utf-8') as file:
      html_content = file.read()
  soup = BeautifulSoup(html_content, 'html.parser')
  product_cards = soup.find_all(class_='product-card')
  return product_cards

d = {"Name": [], "Count_Gamers": [], "Time" : [], "Age":[], "Thematics":[], "Categories":[]}
for g in range(0, 109): # 3 заменить на 109
  product_cards = link_stranicy(g)
  for i in range(len(product_cards)):
    a = product_cards[i]
    d["Name"].append(make_name(a))
    if Count_Gamers_Time_Age(a):
      d["Count_Gamers"].append(Count_Gamers_Time_Age(a)[0])
      if len(Count_Gamers_Time_Age(a)) > 1:
        d["Time"].append(Count_Gamers_Time_Age(a)[1])
        if len(Count_Gamers_Time_Age(a)) > 2:
          d["Age"].append(Count_Gamers_Time_Age(a)[2])
        else:
          d["Age"].append('')
      else:
        d["Time"].append('')
        d["Age"].append('')
    else:
        d["Count_Gamers"].append("")
        d["Time"].append('')
        d["Age"].append('')
    html = get_page_html(find_link(a))
    if html:
      save_html_to_file(html, "boardgamegeek_page_dob_str.html")
    with open('boardgamegeek_page_dob_str.html', 'r', encoding='utf-8') as file:
      html_content_dob = file.read()
    q = Thematics_Categories(html_content_dob)
    if len(q):
      d["Thematics"].append(q[0])
      if len(q) == 2:
        d["Categories"].append(q[1])
      else:
        d["Categories"].append([])
    else:
      d["Thematics"].append([])
      d["Categories"].append([])
    print(i)

df = pd.DataFrame(d)
drive.mount('/content/drive')
df.to_csv('games.csv')
#!cp games.csv /content/drive/MyDrive/

