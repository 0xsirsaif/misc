"""
A command-line tool for downloading books from <nour-books.com>, initially.
>> getbook [options] [book-name] [rename-it]
"""
import requests
import typer
import pathlib
import bs4

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def _tutor_media_bias():
    url = "https://www.allsides.com/media-bias/ratings"
    page_content = requests.get(url).content
    soup = bs4.BeautifulSoup(page_content, "html.parser")
    content_table = soup.select_one("tbody tr")


def _tutor_basic():
    from urllib.request import urlopen
    url: str = "http://olympus.realpython.org/profiles/dionysus"
    html_str: str = urlopen(url).read().decode("utf-8")
    # html_str[name_index: name_index + len("Name:")]
    name_index: int = html_str.find("Name:")
    # html_str[color_index: color_index + len("Favorite Color:")]
    color_index: int = html_str.find("Favorite Color:")


def main(book_title: str, target_dir: pathlib.Path):
    driver = webdriver.Firefox()
    driver.get("https://www.noor-book.com/")
    element = driver.find_element(By.CSS_SELECTOR, ".form-group input").click()
    ActionChains(driver).move_to_element(element).send_keys("CCCC").perform()

    driver.close()


if __name__ == "__main__":
    typer.run(main)
