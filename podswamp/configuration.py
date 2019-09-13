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
        self.enable_guest_pages = self.guest_pages.get("enable_guest_pages", False)
        self.guest_page_strippers = self.guest_pages.get("guest_page_strippers", [])
        self.guest_page_preloaded_entries = self.guest_pages.get("preloaded_entries", [])
        self.guest_page_episode_guest_re = re.compile(self.guest_pages.get("episode_guest_re", ".+[ 0-9]* - (.*)"), re.IGNORECASE)

    def defaulted_folder(self, key, default_location):
        folder = self.config.get(key)
        if folder is None:
            folder = os.path.join(self.podswamp_location, default_location)
        else:
            folder = self.get_project_relative(folder)
        return folder

    def get_template_folder(self):
        return self.defaulted_folder("template_folder", "templates")

    def get_resources_folder(self):
        return self.defaulted_folder("resources_folder", "resources")

    def get_project_relative(self, folder_or_file):
        return os.path.join(self.project_root, folder_or_file)

    def guest_pages_enabled(self):
        return self.enable_guest_pages