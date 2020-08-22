import unittest as ut
from praw.models import ListingGenerator
from praw.models import Submission
from freegamefinder.providers.subreddits import gamedeals as rgd
from freegamefinder.providers.subreddits import freegamefindings as rfgf


class TestSubredditProviders(ut.TestCase):
    def test_get_posts(self):
        """ Tests that Subreddit objects can be created and that praw is able to return valid posts """
        expected_length = 3
        r_gamedeals = rgd.GameDeals(limit=expected_length)
        r_freegamefindings = rfgf.FreeGameFindings(limit=expected_length)
        for sub in [r_gamedeals, r_freegamefindings]:
            posts = sub.get_posts()
            self.assertIsInstance(posts, ListingGenerator)
            for i, post in enumerate(posts):
                self.assertIsInstance(post, Submission)
                self.assertIsNotNone(post.title)
