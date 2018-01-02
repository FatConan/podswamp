#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import pickle
import shutil

from jinja2 import Environment, FileSystemLoader
from podswamp.helpers.progress import Progress
from podswamp.entities import *

class HTMLGenerator:
    html_folder_base = "./html/"
    basic_html_template = 'base.html'
    episode_template = 'episodes/episode.html'
    episodes_template = 'episodes/index.html'
    guests_template = 'guests/index.html'
    homepage_template = 'home/homepage.html'
    guest_template = 'guests/guest.html'
    css_template = 'css/style.css'
    progress = Progress()

    def __init__(self, config):
        self.config = config

        self.env = Environment(loader=FileSystemLoader(config.get_template_folder()))
        self.resources_folder = config.get_resources_folder()
        self.output_folder = self.html_folder_base
        self.channel_data = {}

        with open(os.path.join(config.project_root, 'data/base.json'), 'r') as base_json:
            data = json.load(base_json)
            self.channel_data = data.get("channel", {})

        self.common_content = {
            "title": self.channel_data.get("title", "Untitled Podcast"),
            "podswamp_intro": self.channel_data.get("podswamp_intro", "This is a podswamp generated site for a Libsyn provided podcast."),
            "guest_pages_enabled": self.config.guest_pages_enabled()
        }

        with open(os.path.join(config.project_root, 'data/guests.json'), 'rb') as guest_json:
            self.guests = pickle.load(guest_json)

        with open(os.path.join(config.project_root, 'data/enriched.json'), 'rb') as enriched_data:
            self.episodes = pickle.load(enriched_data)

        self.generate_pages()

    def clean_output_folder(self):
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)

    def render_template(self, template, data, outputfile):
        outputfileFull = os.path.join(self.output_folder, outputfile)
        folderPath = '/'.join(outputfileFull.split('/')[:-1])
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        template = self.env.get_template(template)
        with open(outputfileFull, 'wb') as output:
            output.write(template.render(data).encode("utf8"))

    def patch(self, update_content):
        copy = self.common_content.copy()
        copy.update(update_content)
        return copy

    def generate_index_page(self):
        #Will consist of the top ten episodes
        #Latest episode
        #Link to the recaps
        self.progress.pprint("Writing Index Page")
        sorted_episodes = sorted(list(self.episodes.items()), key=lambda v: v[1].position, reverse=True)
        id, latest = sorted_episodes[0]
        latest.latest = True
        next_index = 1 % len(sorted_episodes)
        prev_episode = sorted_episodes[-1]
        next_episode = sorted_episodes[next_index]

        content = self.patch({
            'episode': latest,
            'classes': 'latest',
            'next': next_episode[1],
            'next_link': '/episodes/%s.html' % next_episode[0],
            'prev': prev_episode[1],
            'prev_link': '/episodes/%s.html' % prev_episode[0],
        })
        self.render_template(self.homepage_template, content, 'index.html')

    def generate_show_pages(self):
        sorted_episodes = sorted(list(self.episodes.items()), key=lambda v: v[1].position, reverse=False)
        for i, deets in enumerate(sorted_episodes):
            id, episode = deets
            prev_index = i-1
            next_index = (i+1) % len(sorted_episodes)
            prev_episode = sorted_episodes[prev_index]
            next_episode = sorted_episodes[next_index]
            context = self.patch({
                'episode': episode,
                'next': next_episode[1],
                'next_link': '/episodes/%s.html' % next_episode[0],
                'prev': prev_episode[1],
                'prev_link': '/episodes/%s.html' % prev_episode[0],
            })

            self.progress.progress_bar(len(self.episodes), i, "Writing Episode Pages ")
            self.render_template(self.episode_template, context, 'episodes/%s.html' % id)

    def generate_guest_pages(self):
        attendance = Attendance(self.episodes)
        for i, deets in enumerate(self.guests.items()):
            name, details = deets
            self.progress.progress_bar(len(self.guests), i, "Writing Guest Pages ")
            if not details.noGuest:
                self.render_template(self.guest_template, self.patch({'guest': details, 'attendance':json.dumps(attendance.getAttendance(details))}), 'guests/%s.html' % details.id)

    def generate_guest_landing_page(self):
        self.progress.pprint("Writing Guest Landing Page")
        guest_entries = []
        for name, details in sorted(self.guests.items(), key=lambda x: x[1].appearances, reverse=True):
            if not details.noGuest:
                guest_entries.append(details)

        content = self.patch({
           'appearances': guest_entries,
        })

        self.render_template(self.guests_template, content, 'guests_index.html')

    def generate_episode_landing_page(self):
        self.progress.pprint("Writing Episode Landing Page")
        content = self.patch({
            'episodes': sorted([episode for episode in self.episodes.values()], key=lambda e: e.position, reverse=True)
        })
        self.render_template(self.episodes_template, content, 'episodes_index.html')

    def clear_and_copy_resources(self):
        self.progress.pprint("Copying Resources")
        html_resources = os.path.join(self.output_folder, "resources")
        if os.path.exists(html_resources):
            shutil.rmtree(html_resources)
        shutil.copytree(self.resources_folder, html_resources)

    def generate_pages(self):
        self.clean_output_folder()
        self.generate_index_page()
        self.generate_show_pages()
        self.generate_episode_landing_page()

        if self.config.guest_pages_enabled():
            self.generate_guest_pages()
            self.generate_guest_landing_page()

        self.clear_and_copy_resources()

if __name__ == "__main__":
    from podswamp.configuration import Config
    install_location = os.path.dirname(__file__)
    htmlGen = HTMLGenerator(Config(os.path.join(install_location, "../"), install_location))



