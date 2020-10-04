import requests
import time
import csv
import itertools
from bs4 import BeautifulSoup
book_name = dict()

header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
search_response=requests.get(url,headers=header)
cookie={}

def get_search(search_query):
    url = "https://www.amazon.in/s?k=" + search_query
    page = requests.get(url, cookies = cookie, headers = header)
    if page.status_code == 200:
        return page
    else:
        return "Error"

def search_asin(asin):
    url = "https://www.amazon.in/dp/" + asin
    print(url)
    page = requests.get(url, cookies = cookie, headers = header)
    if page.status_code == 200:
        return page
    else:
        return "Error"

def search_reviews(review_link):
    url = "https://www.amazon.in"+review_link
    print(url)
    page = requests.get(url, cookies = cookie, headers = header)
    if page.status_code == 200:
        return page
    else:
        return "Error"

for page in range(1, 50):
    data_asin = []
    product_names = []
    response = get_search('s?k=economics+books&page=' + str(page))
    soup = BeautifulSoup(response.content)
    for i in soup.findAll("div",{'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"}):
        data_asin.append(i['data-asin'])
    for i in soup.findAll("span",{'class':'a-size-medium a-color-base a-text-normal'}):
        product_names.append(i.text)

    for i in range(len(data_asin)):
        reviews = []
        response = search_asin(data_asin[i])
        soup = BeautifulSoup(response.content)
        for j in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
            rev = 1
            for rev in range(100):
                flag = 0
                response = Searchreviews(j['href']+'&pageNumber=' + str(rev))
                soup = BeautifulSoup(response.content)
                for rev_per in soup.findAll("span",{'data-hook':"review-body"}):
                    flag = 1
                    reviews.append(rev_per.text)
                if flag == 0:
                    break
        book_name[product_names[i]] = reviews
        time.sleep(10)

with open("scrapping.csv", "w") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(book_name.keys())
    writer.writerows(itertools.zip_longest(*book_name.values()))