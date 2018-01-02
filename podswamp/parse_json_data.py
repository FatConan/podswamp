import json
import re
import pickle
from podswamp.entities import *

class GuestProcessingAndKeywordExtraction:
    #The standard episode titles are in the format Episode XXXX - <Guest Name>
    #It's not 100% clean so we'll need the ability to tweak the entries here. I'm going to specify a
    #lis of special cases (should only be 1 entry at the moment) to handle it.

    episode_guest_re = re.compile(".+[ 0-9]* - (.*)", re.IGNORECASE)
    guest_page_strippers = []
    guest_name_splitter = '|'

    def __init__(self, config=None):
        self.guests = {}
        self.episodes = {}
        self.preloads = []
        self.guest_page_strippers = []

        if config is not None:
            self.episode_guest_re = config.guest_page_episode_guest_re
            self.preloads = config.guest_page_preloaded_entries
            self.guest_page_strippers = config.guest_page_strippers

        for preload in self.preloads:
            #Preload format is ("Alias name (or None)", [("Aliased from name", Should appear as AKA (True or False)),...]
            self.addNewGuest(*preload)

        self.reversedAlias = {}
        for name, guest in self.guests.items():
            for alias, displayedAlias in guest.aliases:
                try:
                    self.reversedAlias[alias].append(guest)
                except KeyError:
                    self.reversedAlias[alias] = [guest]

    def addNewGuest(self, name, aliases=None):
        if name == '':
            name = None

        if not self.guests.get(name):
            self.guests[name] = Guest(name, aliases)
        return self.guests.get(name)

    def addNewEpisode(self, episodeData):
        self.episodes[episodeData.get('episode_id')] = Episode(episodeData)

    def processEpisodes(self):
        with open("data/base.json", "r") as json_file:
            data = json.load(json_file)
            for episodeData in data.get("episodes", []):
                self.addNewEpisode(episodeData)

            for id, episode in self.episodes.items():
                self.processEpisodeGuests(episode)
            for id, episode in self.episodes.items():
                self.postProcessGuestsFromEpisodeDescription(episode)

        self.storeData()

    def postProcessGuestsFromEpisodeDescription(self, episode):
        episodeGuests = episode.guests
        for name, guest in self.guests.items():
            if guest and guest.name.lower() in episode.description.lower():
                episode.addGuest(guest)

        for guestAlias, guests in self.reversedAlias.items():
            if guestAlias and guestAlias.lower() in episode.description.lower():
                for match in guests:
                    episode.addGuest(match)

    def processEpisodeGuests(self, episode):
        guest = ''
        #Try and get the guest name (or names from the episode title)
        processedGuestList = [] #List of potential guest names
        try:
            guest = self.episode_guest_re.findall(episode.title)[0]
        except IndexError:
            guest = ''
        finally:
            for replacement in self.guest_page_strippers:
                guest = guest.replace(replacement, '|')
            guestList = [name for name in guest.split(self.guest_name_splitter) if name != '']
            if not guestList:
                guestList = ['']

            if guestList:
                #Now we should have an array of guest Names, check their no aliases
                for guest in guestList:
                    guest = guest.strip()
                    if self.reversedAlias.get(guest) is not None:
                        for match in self.reversedAlias.get(guest):
                            processedGuestList.append(match)
                    else:
                        processedGuestList.append(self.addNewGuest(guest))

        print("%s @ %s" % (episode.title, ' | '.join([g.name for g in processedGuestList])))
        for guest in processedGuestList:
            episode.addGuest(guest)

    def storeData(self):
        with open("data/guests.json", "wb") as guests_json:
            pickle.dump(self.guests, guests_json)

        with open("data/enriched.json", "wb") as enriched_episodes:
            pickle.dump(self.episodes, enriched_episodes)



#DescriptionAnalyser(extractor.episodes)
if __name__ == "__main__":
    extractor = GuestProcessingAndKeywordExtraction()
    extractor.processEpisodes()


