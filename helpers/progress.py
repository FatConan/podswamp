# coding: utf-8

import sys
import time
import math

class Progress:
    chars = ['|', '/', '—', '\\']

    def __init__(self):
        self.index = 0
        self.stdout = sys.stdout

    def pprint(self, print_string):
        self.stdout.write("%s\r" % print_string)
        self.stdout.flush()

    def percentage(self, progress, progressIndicator="Progress: %d%% "):
        self.stdout.write("%s \r" % (progressIndicator % progress))
        self.stdout.flush()

    def spinner(self, preamble="%s"):
        self.stdout.write("%s\r" % (preamble % self.chars[self.index]))
        self.index = (self.index + 1) % len(self.chars)
        self.stdout.flush()

    def progress_bar(self, total, completed, preamble=""):
        bar_end_left = "["
        bar_end_right = "]"
        waiting_char="="
        complete_char="|"
        length = 20

        complete = int(math.ceil(length * (completed * 1.0)/total))

        self.stdout.write("%s%s%s%s%s\r" % (preamble, bar_end_left, complete_char * complete, waiting_char * (length-complete), bar_end_right))
        self.stdout.flush()

if __name__ == '__main__':
    p = Progress()

    print "\nSpinner"
    for i in range(0, 200):
        p.spinner()
        time.sleep(0.01)

    print "\nBasic Progress"
    for i in range(0, 100):
        p.percentage(i)
        time.sleep(0.01)

    print "\nProgress Bar"
    for i in range(0, 100):
        p.progress_bar(100, i)
        time.sleep(0.01)

