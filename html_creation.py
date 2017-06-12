#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
import json
import os
import pickle
from helpers.progress import Progress
from spy_entities import *
import shutil
from jinja2 import Environment, PackageLoader


class HTMLGenerator:
    version = date.today().strftime("%Y.%m.%d")
    env = Environment(loader=PackageLoader(__name__, 'templates'))

    html_folder_base = "./html/"
    resources_folder = "resources"
    basic_html_template = 'base.html'
    episode_template = 'episodes/episode.html'
    episodes_template = 'episodes/index.html'
    guests_template = 'guests/index.html'
    homepage_template = 'home/homepage.html'
    guest_template = 'guests/guest.html'
    css_template = 'css/style.css'
    progress = Progress()

    def __init__(self):
        self.output_folder = os.path.join(self.html_folder_base, self.version)

        with open('data/guests.json', 'rb') as quest_json:
            self.guests = pickle.load(quest_json)
        with open('data/enriched.json', 'rb') as enriched_data:
            self.episodes = pickle.load(enriched_data)
        self.generate_pages()

    def render_template(self, template, data, outputfile):
        outputfileFull = os.path.join(self.output_folder, outputfile)
        folderPath = '/'.join(outputfileFull.split('/')[:-1])
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        template = self.env.get_template(template)
        with open(outputfileFull, 'wb') as output:
            output.write(template.render(data).encode("utf8"))

    def generate_index_page(self):
        #Will consist of the top ten episodes
        #Latest episode
        #Link to the recaps
        self.progress.pprint("Writing Index Page")
        latest = sorted(self.episodes.values(), key=lambda e: e.position, reverse=True)[0]
        latest.latest = True

        content = {
            'episode': latest,
            'classes': 'latest',
        }
        self.render_template(self.homepage_template, content, 'index.html')

    def generate_show_pages(self):
        for i, deets in enumerate(self.episodes.items()):
            id, episode = deets
            self.progress.progress_bar(len(self.episodes), i, "Writing Episode Pages ")
            self.render_template(self.episode_template, {'episode':episode},'episodes/%s.html' % id)

    def generate_guest_pages(self):
        attendance = Attendance(self.episodes)
        for i, deets in enumerate(self.guests.items()):
            name, details = deets
            self.progress.progress_bar(len(self.guests), i, "Writing Guest Pages ")
            if not details.noGuest:
                self.render_template(self.guest_template, {'guest': details, 'attendance':json.dumps(attendance.getAttendance(details))}, 'guests/%s.html' % details.id)

    def generate_guest_landing_page(self):
        self.progress.pprint("Writing Guest Landing Page")
        guest_entries = []
        for name, details in sorted(self.guests.items(), key=lambda x: x[1].appearances, reverse=True):
            if not details.noGuest:
                guest_entries.append(details)
        content = {
           'appearances': guest_entries,
        }
        self.render_template(self.guests_template, content, 'guests_index.html')

    def generate_episode_landing_page(self):
        self.progress.pprint("Writing Episode Landing Page")
        content = {
            'episodes': sorted([episode for episode in self.episodes.values()], key=lambda e: e.position, reverse=True)
        }
        self.render_template(self.episodes_template, content, 'episodes_index.html')

    def clear_and_copy_resources(self):
        self.progress.pprint("Copying Resources")
        html_resources = os.path.join(self.output_folder, self.resources_folder)
        if os.path.exists(html_resources):
            shutil.rmtree(html_resources)
        shutil.copytree(self.resources_folder, html_resources)

    def generate_pages(self):
        #self.generate_css()
        self.generate_index_page()
        self.generate_show_pages()
        self.generate_guest_pages()
        self.generate_episode_landing_page()
        self.generate_guest_landing_page()
        self.clear_and_copy_resources()

if __name__ == "__main__":
    htmlGen = HTMLGenerator()



