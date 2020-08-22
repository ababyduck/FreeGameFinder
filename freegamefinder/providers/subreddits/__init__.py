from abc import ABC
import praw
from freegamefinder.freebie import Freebie
from freegamefinder.credentials import reddit_api as secrets

REDDIT = praw.Reddit(
    client_id=secrets['client_id'],
    client_secret=secrets['client_secret'],
    user_agent=secrets['user_agent'],
    username=secrets['username'],
    password=secrets['password']
)


class Subreddit(ABC):
    """Abstract base class for subreddit providers"""
    def __init__(self,
                 subreddit: str,
                 limit: int = 100,           # Max number of posts to retrieve (reddit API rate limit is 1000)
                 provider_name: str = None,
                 always_free: bool = False,
                 expired_flair: str = None):
        self.controller = REDDIT.subreddit(subreddit)
        self.always_free = always_free
        if limit > 1000:
            self.limit = 1000
        else:
            self.limit = limit
        if provider_name is None:
            self.provider_name = f"/r/{subreddit}"
        if expired_flair is None:
            self.expired_flair = None
        else:
            self.expired_flair = expired_flair.lower()
        # Compiled regex patterns for basic parsing. Only re_title is strictly required
        self.re_title = None
        self.re_free = None
        self.re_platform = None

    def get_posts(self, sort_by="new"):
        """ Gets posts from the subreddit passed in on instantiation
        :param sort_by: Method to use for retrieving posts: 'new', 'top', or 'hot'
        :return: Praw ListingGenerator object containing reddit posts
        """
        if sort_by == "new":
            return self.controller.new(limit=self.limit)
        elif sort_by == "top":
            return self.controller.top(limit=self.limit)
        elif sort_by == "hot":
            return self.controller.hot(limit=self.limit)
        return None

    def get_freebies(self, posts=None):
        """ Calls get_posts() and returns only the valid free results
        :param posts: (Optional) If a collection of posts is provided it will be used instead of calling get_posts()
        :return: List of Freebie objects constructed from reddit posts
        """
        freebies = []
        # Retrieve posts if they weren't passed in directly
        if posts is None:
            posts = self.get_posts(sort_by="new")
        # Make sure a post is free, non-expired, and has a game title before returning it
        for post in posts:
            if self.post_is_free(post) and not self.post_is_expired(post):
                match_title = self.re_title.search(post.title)
                if match_title:
                    this_post = Freebie(
                        title=match_title.group(0),
                        url=post.url,
                        provider=f"{self.provider_name} ({post.shortlink})"
                    )
                    match_platform = self.re_platform.search(post.title)
                    if match_platform:
                        this_post.platform = match_platform.group(0)
                    freebies.append(this_post)
        return freebies

    def post_is_expired(self, post):
        """ Returns True of post has known "expired" flair """
        if self.expired_flair:
            try:
                return self.expired_flair == post.link_flair_text.lower()
            except AttributeError:
                pass
        return False

    def post_is_free(self, post):
        """ Returns True if post appears to reference a free game """
        if self.always_free:
            return True
        elif self.re_free:
            return self.re_free.search(post.title.lower())
        return False
