#!/usr/bin/env python
# -*- coding: utf-8 -*-

from podswamp.html_creation import HTMLGenerator
from podswamp.scraper import FeedParser
from podswamp.parse_json_data import GuestProcessingAndKeywordExtraction


def process_from_config(config):
    feed_parser = FeedParser(config.rss)
    feed_parser.parse_feed(True)

    extractor = GuestProcessingAndKeywordExtraction()
    extractor.processEpisodes()

    HTMLGenerator(config)

