from dateutil import parser

class Episode:
    def __init__(self, episodeData):
        self.position = episodeData.get('position', -1)
        self.episode_id = episodeData.get('episode_id', '')
        self.title = episodeData.get('title', '')
        self.published = parser.parse(episodeData.get('published', ''))
        self.link = episodeData.get('link', '')
        self.description = episodeData.get('description', '')
        self.slug = episodeData.get('slug', '')

        self.media_url = episodeData.get('media_url', '')
        self.media_type = episodeData.get('media_type', '')
        self.media_length = episodeData.get('media_length', '')

        self.duration = episodeData.get('duration', '')
        self.keywords = episodeData.get('keywords', [])

        self.guests = []

    def getGuests(self):
        return sorted([g for g in self.guests if not g.noGuest], key=lambda g: g.name)

    def addGuest(self, guest):
        if guest is not None:
            guest.addEpisode(self)
        if guest is not None and guest not in self.guests:
            self.guests.append(guest)