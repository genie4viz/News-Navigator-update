# google_news.py

import feedparser
from dateparser import parse as parse_date
import urllib.parse
import aiohttp
import asyncio

class GoogleNews:
    def __init__(self, lang='en', country='US'):
        self.lang = lang.lower()
        self.country = country.upper()
        self.BASE_URL = 'https://news.google.com/rss'

    def __ceid(self):
        """Compile correct country-lang parameters for Google News RSS URL"""
        return f'?ceid={self.country}:{self.lang}&hl={self.lang}&gl={self.country}'

    def __search_helper(self, query):
        return urllib.parse.quote_plus(query)

    def __from_to_helper(self, date_str):
        try:
            return parse_date(date_str).strftime('%Y-%m-%d')
        except Exception as e:
            print(f"Error parsing date: {e}")
            raise

    async def __parse_feed(self, feed_url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(feed_url) as response:
                    if response.status != 200:
                        raise Exception(f"Error fetching the feed: {response.status}")

                    text = await response.text()
                    d = feedparser.parse(text)
                    return {'entries': d.get('entries', [])}
        except Exception as e:
            print(f"Error in __parse_feed: {e}")
            return {'entries': []}

    def search(self, query: str, helper=True, when=None, from_=None, to_=None):
        """
        Return a list of all articles given a full-text search parameter,
        a country, and a language
        """
        if when:
            query += f' when:{when}'
        if from_:
            from_ = self.__from_to_helper(from_)
            query += f' after:{from_}'
        if to_:
            to_ = self.__from_to_helper(to_)
            query += f' before:{to_}'
        if helper:
            query = self.__search_helper(query)

        search_ceid = self.__ceid().replace('?', '&')
        feed_url = f'{self.BASE_URL}/search?q={query}{search_ceid}'
        return asyncio.run(self.__parse_feed(feed_url))
