from blogs.parsability import Scraper
from blogs.models import Article, Blog
from urllib.request import urlopen, Request as req
import vcr
from datetime import datetime
from time import mktime
from bs4 import BeautifulSoup
import feedparser
from utils.s3_utils import get_object, put_object, upload_file, get_location, BUCKET_NAME, upload_article, create_article_url
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/41.0.2228.0 Safari/537.3'}

def is_last_page(soup):

    navigation = soup.find('div', attrs={"class": "navigation"})

    next_li = navigation.find('li', attrs={"class": "pagination-next"})

    if next_li is None:
        return True

    return False

class StratecheryScraper(Scraper):
    def __init__(self,
                 name_id="stratechery",
                 rss_url="https://stratechery.com/feed/",
                 home_url="https://stratechery.com"):

        super().__init__(name_id=name_id, rss_url=rss_url, home_url=home_url)


    def _poll(self):
        self.standard_rss_poll()

    # USE WITH PROXY FLEET TO PREVENT RATE LIMITS
    def get_all_posts(self, page):
        pass