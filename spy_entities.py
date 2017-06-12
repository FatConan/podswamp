import hashlib
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from dateutil import parser
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

class DescriptionAnalyser:
    def __init__(self, episodes):
        self.episodes = episodes
        self.documentTerms = self.getWords(' '.join([episode.description for episode in self.episodes.values()]))
        self.documentFrequency = self.getCounts(self.documentTerms)

        for episode in self.episodes.values():
            episode.terms = self.getWords(episode.description)
            episode.termFrequencies = self.getCounts(episode.terms)

        for episode in self.episodes.values():
            for term in episode.terms:
                self.getTF_IDF(term)

    def getTF_IDF(self, term):
        N = len(self.episodes)
        frequencies = []
        for episode in self.episodes.values():
            if term in episode.terms:
                frequencies.append((episode, episode.termFrequencies.get(term, 0)))

        idf = N/(1 + len(frequencies))
        for episode, tf in frequencies:
            print("%s, %s, %s, %s" % (episode.title, term, idf,  tf * idf))

    def removeStopwords(self, word_list):
        return [w for w in word_list if w not in stopwords.words('english')]

    def getCounts(self, words):
        counts = Counter(words)
        for word, count in counts.most_common():
            if count == 1:
                del counts[word]
            else:
                counts[word] = 1
        return counts

    def getWords(self, content):
        words = content.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(words)
        words = self.removeStopwords(words)
        return words

class Attendance:
    def __init__(self, episodes):
        self.episodes = episodes

    def getAttendance(self, guest):
        dates = [episode.published for episode in sorted(self.episodes.values(), key=lambda e: e.position)]
        attended_dates = [ep.published for ep in guest.episodes]
        mean_attendance = (100.0 * len(attended_dates))/(1.0 * len(dates))
        attended = [{'date':d.strftime("%Y-%m-%d"), 'present': int(d in attended_dates), 'mean_attendance':mean_attendance} for d in dates]

        attendance = 0
        for i, entry in enumerate(attended):
            if entry['present'] or i == 0 or i == (len(attended) - 1):
                attendance += entry['present']
                entry['running_mean'] = (attendance * 100.0)/(i+1) # - mean_attendance

        return attended

class Guest:
    def __init__(self, name, aliases=None):
        if name is None:
            self.name = '[No Guest]'
            self.noGuest = True
        else:
            self.name = name
            self.noGuest = False

        self.episodes = []
        self.id = hashlib.sha224(self.name).hexdigest()

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
        last_episode = self.sortedEpisodes[0]
        distance = datetime.now(utc) - last_episode.published
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

class Episode:
    def __init__(self, episodeData):
        self.position = episodeData.get('position', -1)
        self.episode_id = episodeData.get('episode_id', '')
        self.title = episodeData.get('title', '')
        self.published = parser.parse(episodeData.get('published', ''))
        self.link = episodeData.get('link', '')
        self.description = episodeData.get('description', '')

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