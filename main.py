import requests
from bs4 import BeautifulSoup
import lxml
import csv
import fake_useragent

url = "https://bvbalyans.kz" #основной url
	
with open("index.html", "r", encoding="utf-8") as f:
	f = f.read()# url категорий
links = BeautifulSoup(f, "lxml").find_all("div", class_="h2") # Все ссылки категорий
user_agent = fake_useragent.UserAgent() # User Agent
for link in links:

	link_1 = "https://bvbalyans.kz/" + link.find("a").get("href") # ссылка категорий
	response_1 = requests.get(link_1, headers = {"User-Agent": user_agent.random}).text # get запрос на категорию
	category_cards = BeautifulSoup(response_1, "lxml") #Карточка подкатегорий
	img = url + category_cards.find("div", class_="category-card__img").find("img").get("src")
	category_cards = category_cards.find_all("div", class_="category-list__item")



	try:
		for card in category_cards:
		
			name_category = card.find("a", class_="category-card__title").text # название категорий
			link_2 = url + card.find("a", class_="category-card__title").get("href") # ссылка на подкатегорию
			print(link_2)
			
			response_2 = requests.get(link_2, headers = {"User-Agent": user_agent.random}) # Get запрос на подкатегорию
			bs = BeautifulSoup(response_2.text, "lxml") #BeautifulSoup страницы

			

			bs_1 = bs.find("ul", class_="pagination-list").find_all("li") # проверка на количество страниц

			if len(bs_1) == 1:
				site_len = 1		
				all_card = bs.find("table", class_="listing-result__table").find("tbody").find_all("tr") # все товары с данными
				for card_2 in all_card:
					name_tovar = card_2.find("td", class_="listing-result__type").text.strip() #Название товара
					link_3 = card_2.find("td", class_="listing-result__type").find("a").get("href")

					try:
						standart = card_2.find("td", class_="listing-result__gost").fing("a").text.strip() # стандарт
					except Exception as e:
						standart = ""

					try:
						attributes = BeautifulSoup(response_3, "lxml").find("p", class_="specialoffer-detail__desc").find_next("p").text.strip()
						
					except Exception as e:
						attributes = ""
					try:

						mark = BeautifulSoup(response_3, "lxml").find("div", class_="specialoffer-detail__characteristics-list flex").find_all("span")[-1].text.replace("Марка: ", "")
					except Exception as e:
						mark = ""

					with open("result.csv", "a", encoding="utf-8") as cs:
						writer = csv.writer(cs)
						writer.writerow(
							(
								name_category,
								name_tovar,
								img,
								standart,
								mark,
								attributes
								)
							)
					print(		name_category,
								name_tovar,
								img,
								standart,
								mark,
								attributes								
						)
			elif len(bs_1) > 1:
				site_len = int(bs_1[-1].find("a").text)
				i = 1
				while i < int(site_len):
					response_4 = requests.get(url = link_2 + "page/" + str(i) + "/marka/%20/gost/%20/s1/0/s2/0/s3/0/")
					bs_site = BeautifulSoup(response_4.text, "lxml")
					all_card = bs_site.find("table", class_="listing-result__table").find("tbody").find_all("tr") # все товары с данными
					for card_2 in all_card:
						name_tovar = card_2.find("td", class_="listing-result__type").text.strip()
						link_3 = url + card_2.find("td", class_="listing-result__type").find("a").get("href")

						try:
							standart = card_2.find("td", class_="listing-result__gost").find("a").text.strip()
						except Exception as e:
							standart = ""
						response_3 = requests.get(link_3, headers = {"User-Agent": user_agent.random}).text
						try:
							attributes = BeautifulSoup(response_3, "lxml").find("p", class_="specialoffer-detail__desc").find_next("p").text.strip()
							
						except Exception as e:
							attributes = ""
						try:

							mark = BeautifulSoup(response_3, "lxml").find("div", class_="specialoffer-detail__characteristics-list flex").find_all("span")[-1].text.replace("Марка: ", "")
						except Exception as e:
							mark = ""
			
						with open("result.csv", "a", encoding="utf-8") as cs:
							writer = csv.writer(cs)
							writer.writerow(
								(
									name_category,
									name_tovar,
									img,
									standart,
									mark,
									attributes
									)
								)
						print(		name_category,
									name_tovar,
									img,
									standart,
									mark,
									attributes,
									site_len,
									i
							)			
					i+=1
				
	except Exception as e:
		print(link_2 + " - " + name_category)					
