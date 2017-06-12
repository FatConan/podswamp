#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper import FeedParser
from parse_json_data import GuestProcessingAndKeywordExtraction
from html_creation import HTMLGenerator

feedParser = FeedParser()
feedParser.parseFeed(True)

extractor = GuestProcessingAndKeywordExtraction()
extractor.processEpisodes()

htmlGen = HTMLGenerator()
