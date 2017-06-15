import os
import json


class Config:


    def __init__(self, project_root, podswamp_location):
        self.project_root = project_root
        self.podswamp_location = podswamp_location

        with open(os.path.join(project_root, "project.json"), "r") as json_config:
            self.config = json.load(json_config)
            self.rss = self.config.get("rss")

    def get_template_folder(self):
        return self.config.get("template_folder", os.path.join(self.podswamp_location, 'templates'))
