import xml.etree.ElementTree  as ET
from unittest                                                                                       import TestCase
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Parser                 import Hacker_News__Parser
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article  import Model__Hacker_News__Article
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed     import Model__Hacker_News__Feed

class test_Hacker_News__Parser(TestCase):

    def setUp(self):
        self.parser      = Hacker_News__Parser()
        self.sample_xml  = '''<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/">
                <channel>
                    <title>The Hacker News</title>
                    <link>https://thehackernews.com</link>
                    <description>Security News</description>
                    <language>en-us</language>
                    <lastBuildDate>Thu, 05 Dec 2024 01:33:01 +0530</lastBuildDate>
                    <sy:updatePeriod>hourly</sy:updatePeriod>
                    <sy:updateFrequency>1</sy:updateFrequency>
                    <item>
                        <title>Test Article</title>
                        <description><![CDATA[Test Description]]></description>
                        <link>https://thehackernews.com/2024/12/test-article.html</link>
                        <guid>https://thehackernews.com/2024/12/test-article.html</guid>
                        <pubDate>Wed, 04 Dec 2024 22:53:00 +0530</pubDate>
                        <author>info@thehackernews.com (The Hacker News)</author>
                        <enclosure url="https://example.com/image.jpg" type="image/jpeg" length="12216320"/>
                    </item>
                </channel>
            </rss>'''

    def test_setup(self):
        with self.parser as target:
            target.setup(self.sample_xml)
            assert isinstance(target.root, ET.Element)
            assert target.xml_content   == self.sample_xml
            assert target.channel       is not None

    def test_parse_feed(self):
        with self.parser as target:
            target.setup(self.sample_xml)
            feed = target.parse_feed()
            assert isinstance(feed, Model__Hacker_News__Feed)
            assert feed.title == "The Hacker News"
            assert feed.link == "https://thehackernews.com"
            assert feed.language == "en-us"
            assert feed.update_period == "hourly"
            assert feed.update_frequency == 1

    def test_parse_articles(self):
        with self.parser as target:
            target.setup(self.sample_xml)
            articles = target.parse_articles()
            assert isinstance(articles, list)
            assert len(articles) == 1
            assert isinstance(articles[0], Model__Hacker_News__Article)

    def test_parse_article(self):
        with self.parser as target:
            target.setup(self.sample_xml)
            item = target.channel.find('item')
            article = target.parse_article(item)
            assert isinstance(article, Model__Hacker_News__Article)
            assert article.title == "Test Article"
            assert article.description == "Test Description"
            assert article.link == "https://thehackernews.com/2024/12/test-article.html"
            assert article.image_url == "https://example.com/image.jpg"

    def test_error_handling(self):
        with self.parser as target:
            with self.assertRaises(ET.ParseError):
                target.setup('<rss><channel><title>Test</title></channel>')

    def test_missing_elements(self):
        with self.parser as target:
            minimal_xml = '''<?xml version="1.0"?>
                <rss><channel>
                    <item>
                        <title>Test</title>
                        <link>http://test.com</link>
                    </item>
                </channel></rss>'''
            target.setup(minimal_xml)
            feed = target.parse_feed()
            assert isinstance(feed, Model__Hacker_News__Feed)
            assert feed.title == ""
            articles = feed.articles
            assert len(articles) == 1
            assert articles[0].title == "Test"
            assert articles[0].description == ""
            assert articles[0].author == ""

    def test_get_element_text(self):
        with self.parser as target:
            target.setup(self.sample_xml)
            assert target.get_element_text(target.channel, 'title') == "The Hacker News"
            assert target.get_element_text(target.channel, 'nonexistent') == ""
            assert target.get_element_text(target.channel, 'nonexistent', 'default') == "default"