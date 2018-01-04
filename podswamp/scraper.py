#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import json
from xml.dom.minidom import parseString
from podswamp.entities import *
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self, strip=False):
        HTMLParser.__init__(self)
        self.reset()
        self.strip = strip
        self.fed = []

    def handle_starttag(self, tag, attrs):
        if not self.strip:
            self.fed.append("<%s>" % tag)

    def handle_endtag(self, tag):
        if not self.strip:
            self.fed.append("</%s>" % tag)

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper(strip=True)
    s.feed(html)
    return s.get_data()


def clean_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class FeedParser:
    def __init__(self, config):
        self.libsyn_feed = config.rss
        self.config = config

        self.data = {
            "channel": {},
            "episodes": []
        }

        self.loaded_data = {
            "channel": {},
            "episodes": []
        }

    def parse_feed(self, update=False):
        if update:
            existing_entries = self.get_existing_entries()
        else:
            existing_entries = {}

        response = requests.get(self.libsyn_feed)
        xml_document = parseString(response.content)

        self.handle_episodes_list(xml_document, existing_entries)
        self.store_data()

    def get_existing_entries(self):
        entry_ids = {}
        if os.path.exists(self.config.get_project_relative("data/base.json")):
            with open(self.config.get_project_relative("data/base.json"), "r") as json_file:
                self.loaded_data = json.load(json_file)
                for entry in self.loaded_data["episodes"]:
                    entry_ids[entry.get('episode_id')] = True

        return entry_ids

    def get_element_text(self, elements):
        return ''.join([x.data for x in elements[0].childNodes])

    def generate_hashed_id(self, published_date, title):
        string = "%s%s" % (published_date, title)
        return hashlib.sha224(string.encode("utf8")).hexdigest()

    def handle_episodes_list(self, episodes, existing_entries={}):
        channel = episodes.getElementsByTagName("channel")
        channel_title = self.get_element_text(channel[0].getElementsByTagName("title"))
        self.data["channel"]["title"] = channel_title

        items = channel[0].getElementsByTagName("item")
        size = len(items)

        for i, item in enumerate(items):
            title = self.get_element_text(item.getElementsByTagName("title"))
            published = self.get_element_text(item.getElementsByTagName("pubDate"))
            episode_id = self.generate_hashed_id(published, title)

            if not existing_entries.get(episode_id, False):
                entry = {
                    'position': size - i,
                    'episode_id': episode_id,
                    'title':  title,
                    'published': published,
                    'link':  self.get_element_text(item.getElementsByTagName("link")),
                    'stripped_description': strip_tags(self.get_element_text(item.getElementsByTagName("description"))),
                    'description': clean_tags(self.get_element_text(item.getElementsByTagName("description"))),
                    'media_url': item.getElementsByTagName("enclosure")[0].attributes["url"].value,
                    'media_length': item.getElementsByTagName("enclosure")[0].attributes["length"].value,
                    'media_type': item.getElementsByTagName("enclosure")[0].attributes["type"].value,
                    'duration': self.get_element_text(item.getElementsByTagName("itunes:duration")),
                    'keywords': self.get_element_text(item.getElementsByTagName("itunes:keywords")),
                }
                self.data["episodes"].append(entry)
           
    def store_data(self):
        self.loaded_data["channel"] = self.data["channel"]
        self.loaded_data["episodes"] += self.data["episodes"]
        self.data = self.loaded_data

        if not os.path.exists(self.config.get_project_relative("data/")):
            os.mkdir(self.config.get_project_relative("data/"))

        with open(self.config.get_project_relative("data/base.json"), "w") as json_file:
            json.dump(self.loaded_data, json_file)
