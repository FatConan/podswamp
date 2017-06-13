import json
import re
import pickle
from podswamp.entities import *

class GuestProcessingAndKeywordExtraction:
    #The standard episode titles are in the format Episode XXXX - <Guest Name>
    #It's not 100% clean so we'll need the ability to tweak the entries here. I'm going to specify a
    #lis of special cases (should only be 1 entry at the moment) to handle it.

    episode_guest_re = re.compile(".+[ 0-9]* - (.*)", re.IGNORECASE)
    old_episode_number_re = re.compile("(ep\.[ 0-9]*)", re.IGNORECASE)
    guest_name_strippers = ['LIVE from Very Very Fun Day in Chicago',' from JFL Northwest', 'LIVE, with ', 'LIVE with ',
                            'LIVE from MaxFunCon 2014 with ', 'LIVE from MaxFunCon with',
                            'LIVE from MaxFunCon East', 'LIVE from Toronto with',
                            'LIVE from Victoria with ',
                            'from the Northwest Podcast Fest', 'LIVE from the Canadian Comedy Awards',
                            'LIVE from Edmonton with ', 'LIVE from Edmonton',
                            'LIVE from Calgary', 'Switcheroo Week with ',
                            ',', ' and ']
    guest_name_splitter = '|'

    def __init__(self):
        self.guests = {}
        self.episodes = {}

        self.addNewGuest('John Beuhler')
        self.addNewGuest("Graham's dad")
        self.addNewGuest("Ryan Belleville")
        self.addNewGuest('Pete Johansson',[('Pete and Courtney Johansson', False)])
        self.addNewGuest('Courtney Johansson',[('Pete and Courtney Johansson', False)])
        self.addNewGuest(None, [('EVERY SEGMENT!', False), ('', False), ('The Sunday Service', False), ('Pete', False)])
        self.addNewGuest('Abby Shumka', [('Abby Campbell', True)])
        self.addNewGuest('Cam MacLeod', [('Cam Macleod', False)])
        self.addNewGuest('Erica Sigurdson', [('Ricky Dawn Sigurdson', True)])
        self.addNewGuest('Taz VanRassel', [('6 members of The Sunday Service', False)])
        self.addNewGuest('Ryan Beil',[('6 members of The Sunday Service', False)])
        self.addNewGuest('Kevin Lee',[('6 members of The Sunday Service', False)])
        self.addNewGuest('Emmett Hall',[('6 members of The Sunday Service', False)])
        self.addNewGuest('Craig Anderson', [('6 members of The Sunday Service', False)])
        self.addNewGuest('Aaron Read',[('6 members of The Sunday Service', False)])

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
            for episodeData in json.load(json_file):
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
            processed_title = self.old_episode_number_re.sub('', episode.title)
            guest = self.episode_guest_re.findall(processed_title)[0]
        except IndexError:
            guest = ''
        finally:
            for replacement in self.guest_name_strippers:
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

