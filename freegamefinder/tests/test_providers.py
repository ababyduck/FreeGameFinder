import unittest as ut
from random import randint
from praw.models import ListingGenerator
from praw.models import Submission
from freegamefinder.freebie import Freebie
from freegamefinder.providers.subreddits import Subreddit
from freegamefinder.providers.subreddits import gamedeals as rgd
from freegamefinder.providers.subreddits import freegamefindings as rfgf


class TestSubredditProviders(ut.TestCase):
    def test_create_subreddits(self):
        """ Verifies Subreddit objects can be created """
        r_gamedeals = rgd.GameDeals()
        self.assertIsInstance(r_gamedeals, Subreddit)
        self.assertEqual(r_gamedeals.provider_name[3:].lower(),
                         r_gamedeals.controller.display_name.lower())

        r_freegamefindings = rfgf.FreeGameFindings()
        self.assertIsInstance(r_freegamefindings, Subreddit)
        self.assertEqual(r_freegamefindings.provider_name[3:].lower(),
                         r_freegamefindings.controller.display_name.lower())

    def test_get_posts(self):
        """ Verifies praw generates the expected objects """
        r_gamedeals = rgd.GameDeals()
        r_gamedeals.limit = randint(1, 3)
        counter = 0
        posts = r_gamedeals.get_posts()
        self.assertIsInstance(posts, ListingGenerator)
        for post in posts:
            self.assertIsInstance(post, Submission)
            self.assertIsNotNone(post.title)
            post_attributes = post.__dict__.keys()
            for attribute in ["title", "url"]:
                self.assertIn(attribute, post_attributes)
            counter += 1
        self.assertEqual(counter, r_gamedeals.limit)

    def test_get_freebies(self):
        """ Creates 10 Freebies from a subreddit with always_free flag """
        r_freegamefindings = rfgf.FreeGameFindings(limit=10)
        for game in r_freegamefindings.get_freebies():
            self.assertIsInstance(game, Freebie)
