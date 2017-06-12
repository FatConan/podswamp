#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import json
from xml.dom.minidom import parseString
from spy_entities import *
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class FeedParser:
    #libsyn_feed = "http://stoppodcastingyourself.libsyn.com/rss"

    def __init__(self, libsyn_feed):
        self.libsyn_feed = libsyn_feed
        self.data = []
        self.loaded_data = []

    def parseFeed(self, update=False):
        #parse the rss feed, if up date is set to True, we will only process new entries in the feed,
        #otherwise we'll do it all
        if update:
            existing_entries = self.getExistingEntries()
        else:
            existing_entries = {}

        response = requests.get(self.libsyn_feed)
        xml_document = parseString(response.content)

        self.handleEpisodesList(xml_document, existing_entries)
        self.storeData()

    def getExistingEntries(self):
        entry_ids = {}
        if os.path.exists("data/base.json"):
            with open("data/base.json", "r") as json_file:
                self.loaded_data = json.load(json_file)
                for entry in self.loaded_data:
                    entry_ids[entry.get('episode_id')] = True

        return entry_ids


    #join the text nodes from the xml element
    def getElementText(self, elements):
        return ''.join([x.data for x in elements[0].childNodes])

    def generateHashedId(self, published_date, title):
        string = "%s%s" % (published_date, title)
        return hashlib.sha224(string.encode("utf8")).hexdigest()

    #Read the channel, and putt the items (episodes) from the dom
    def handleEpisodesList(self, episodes, existing_entries={}):
        channel = episodes.getElementsByTagName("channel")
        items = channel[0].getElementsByTagName("item")
        size = len(items)

        for i, item in enumerate(items):
            title = self.getElementText(item.getElementsByTagName("title"))
            published = self.getElementText(item.getElementsByTagName("pubDate"))
            episode_id = self.generateHashedId(published, title)

            if not existing_entries.get(episode_id, False):
                print("Saving new entry %s" % episode_id)
                entry = {
                    'position': size - i,
                    'episode_id': episode_id,
                    'title':  title,
                    'published': published,
                    'link':  self.getElementText(item.getElementsByTagName("link")),
                    'description': strip_tags(self.getElementText(item.getElementsByTagName("description"))),
                    'media_url': item.getElementsByTagName("enclosure")[0].attributes["url"].value,
                    'media_length': item.getElementsByTagName("enclosure")[0].attributes["length"].value,
                    'media_type': item.getElementsByTagName("enclosure")[0].attributes["type"].value,
                    'duration': self.getElementText(item.getElementsByTagName("itunes:duration")),
                    'keywords': self.getElementText(item.getElementsByTagName("itunes:keywords")),
                }
                self.data.append(entry)
            else:
                print("Skipping stored entry %s" % episode_id)

    def storeData(self):
        self.loaded_data += self.data
        self.data = self.loaded_data

        if not os.path.exists("data/"):
            os.mkdir("data/")

        with open("data/base.json", "w") as json_file:
            json.dump(self.loaded_data, json_file)

if __name__ == "__main__":
    scraper = FeedParser("http://thedeadauthorspodcast.libsyn.com/rss")
    scraper.parseFeed(True)
