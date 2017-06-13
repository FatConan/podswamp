#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from podswamp.html_creation import HTMLGenerator
from podswamp.scraper import FeedParser
from podswamp.parse_json_data import GuestProcessingAndKeywordExtraction

#libsyn_feed = "http://stoppodcastingyourself.libsyn.com/rss"
libsyn_feed = "http://thedeadauthorspodcast.libsyn.com/rss"

feedParser = FeedParser(libsyn_feed)
feedParser.parseFeed(True)

extractor = GuestProcessingAndKeywordExtraction()
extractor.processEpisodes()

htmlGen = HTMLGenerator()
