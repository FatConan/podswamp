import re

episode_guest_re = re.compile(".+ [0-9]* - (.*)", re.IGNORECASE)
old_episode_number_re = re.compile("(ep\.[ 0-9]*)", re.IGNORECASE)

tests = [
    'Episode 346 - Christina Walkinshaw',
    'Bonus Episode - LIVE from the Canadian Comedy Awards',
    'Stop Podcasting Yourself - ep.6',
    'Episode 130 - LIVE, with John Keister',
]

for test in tests:
    print "%s,%s,%s" % (test, old_episode_number_re.sub('', test), episode_guest_re.findall(old_episode_number_re.sub('', test)))