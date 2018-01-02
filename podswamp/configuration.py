import os
import json
import re

class Config:
    def __init__(self, project_root, podswamp_location):
        self.project_root = project_root
        self.podswamp_location = podswamp_location

        try:
            with open(os.path.join(project_root, "project.json"), "r") as json_config:
                self.config = json.load(json_config)
        except FileNotFoundError:
            print("Not project.json file found")
            self.config = {}

        self.rss = self.config.get("rss")
        self.guest_pages = self.config.get("guest_pages", {})
        self.enable_guest_pages = self.guest_pages.get("enable_guest_pages", True)
        self.guest_page_strippers = self.guest_pages.get("guest_page_strippers", [])
        self.guest_page_preloaded_entries = self.guest_pages.get("preloaded_entries", [])
        self.guest_page_episode_guest_re = re.compile(self.guest_pages.get("episode_guest_re", ".+[ 0-9]* - (.*)"), re.IGNORECASE)

    def get_template_folder(self):
        return self.config.get("template_folder", os.path.join(self.podswamp_location, 'templates'))

    def get_resources_folder(self):
        return self.config.get("resources_folder", os.path.join(self.podswamp_location, 'resources'))

    def guest_pages_enabled(self):
        return self.enable_guest_pages