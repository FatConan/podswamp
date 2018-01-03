from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter

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