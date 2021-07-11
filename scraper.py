from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests


def main():
    #driver = webdriver.Chrome("/usr/bin/chromedriver")
    #driver.get("https://docs.oracle.com/javase/7/docs/api/")

    response = requests.get('https://docs.oracle.com/javase/7/docs/api/allclasses-frame.html')

    #content = driver.page_source
    soup = BeautifulSoup(response.text, 'lxml')
    cc = soup.find('frameset', title_='Packages')
    print(cc)

if __name__ == '__main__':
    main()
    