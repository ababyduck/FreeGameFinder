import unittest as ut
from random import randint
from praw.models import ListingGenerator
from praw.models import Submission
from freegamefinder.providers.subreddits import gamedeals as rgd
from freegamefinder.providers.subreddits import freegamefindings as rfgf


class TestSubredditProviders(ut.TestCase):
    def test_get_posts(self):
        """ Tests that Subreddit objects can be created and that
        praw retrieves the expected number of valid posts
        """
        r_gamedeals = rgd.GameDeals()
        r_freegamefindings = rfgf.FreeGameFindings()
        for sub in [r_gamedeals, r_freegamefindings]:
            sub.limit = randint(1, 3)
            counter = 0
            posts = sub.get_posts()
            self.assertIsInstance(posts, ListingGenerator)
            for post in posts:
                self.assertIsInstance(post, Submission)
                self.assertIsNotNone(post.title)
                counter += 1
            self.assertEqual(counter, sub.limit)
