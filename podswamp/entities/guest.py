import hashlib
from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO

  def tzname(self, dt):
    return "UTC"

  def dst(self, dt):
    return ZERO

utc = UTC()

class Guest:
    def __init__(self, name, slug, aliases=None):
        if name is None:
            self.name = '[No Guest]'
            self.slug = slug
            self.noGuest = True
        else:
            self.name = name
            self.slug = slug
            self.noGuest = False

        self.episodes = []
        self.id = hashlib.sha224(self.name.encode("utf8")).hexdigest()

        if aliases is None:
            self.aliases = []
        else:
            self.aliases = aliases

    @property
    def displayAliases(self):
        return [alias[0] for alias in self.aliases if alias[1]]

    @property
    def appearances(self):
        return len(self.episodes)

    @property
    def sortedEpisodes(self):
        return sorted(self.episodes, key=lambda e: e.position, reverse=True)

    @property
    def timeSinceLastAppearance(self):
        try:
            last_episode = self.sortedEpisodes[0]
            distance = datetime.now(utc) - last_episode.published
        except IndexError:
            distance = 0
        return distance

    @property
    def formattedTimeSinceLastAppearance(self):
        distance = self.timeSinceLastAppearance
        if distance.days < 14:
            return "%d days ago" % distance.days
        elif distance.days >= 14 and distance.days < 40:
            return "%d weeks ago" % (distance.days/7)
        elif distance.days >= 40 and distance.days < 365:
            return "%d months ago" % (distance.days/30)
        else:
            return "%d years ago" % (distance.days/365)


    def addEpisode(self, episode):
        if episode and episode not in self.episodes:
            self.episodes.append(episode)

    def getAsDict(self):
        return {
            'name': self.name,
            'id': self.id,
            'appearances': self.appearances,
            'episodes': self.episodes
        }
