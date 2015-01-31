from re import search

from PyMarkovTextGenerator import Markov
from twitter import Twitter, OAuth

from settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


punctuation = (".", "?", "!")


class TweetBot(object):
    def __init__(self, text_file):
        self.markov_dictionary = Markov()
        with open(text_file) as file:
            self.markov_dictionary.parse(file.read())

    def _end(self, sentance):
        last_word = sentance.split()[-1:]
        if (sentance[-1:] in punctuation
                and len(sentance.split()) > 10
                and last_word not in ("Mr.", "St.")):
            return True
        else:
            return False

    def cleanup_tweet(self, tweet):
        """
        Does a variety of things to beautify the markov-ed text.
        """
        # Fix quotes
        # Remove two quotes separated by a space.
        tweet = tweet.replace('" "', ' ')
        # If the first quote has a space after, put a quote at the beginning of the line.
        if search(r'^[^"]+" ', tweet):
            tweet = '"' + tweet
        # If the last quote on the line has a space before it put a quote at the end of the line.
        if search(r' "[^"]+$', tweet):
            tweet = tweet + '"'

        return tweet

    def generate_tweet(self):
        tweet = ""
        while tweet == "" or len(tweet) > 135:
            tweet = self.markov_dictionary.generate(endf=self._end)
        tweet = self.cleanup_tweet(tweet)
        return tweet


if __name__ == '__main__':
    bot = TweetBot('mobydick.txt')
    twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    twitter.statuses.update(status=bot.generate_tweet())
