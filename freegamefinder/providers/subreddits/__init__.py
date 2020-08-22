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
    def __init__(self, subreddit, provider_name=None, always_free=False, expired_flair=None):
        self.controller = REDDIT.subreddit(subreddit)
        self.provider_name = f"/r/{subreddit}"
        self.always_free = always_free
        if expired_flair is None:
            self.expired_flair = expired_flair
        else:
            self.expired_flair = expired_flair.lower()
        # Compiled regex patterns for basic parsing. Only re_title is strictly required
        self.re_title = None
        self.re_free = None
        self.re_platform = None

    def get_posts(self, sort_by="new", limit=100):
        if sort_by == "new":
            return self.controller.new(limit=limit)
        elif sort_by == "top":
            return self.controller.top(limit=limit)
        elif sort_by == "hot":
            return self.controller.hot(limit=limit)
        return None

    def get_freebies(self, posts=None, limit=100):
        freebies = []
        # Retrieve posts if they weren't passed in directly
        if posts is None:
            posts = self.get_posts(sort_by="new", limit=limit)
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
        if self.expired_flair:
            try:
                return self.expired_flair == post.link_flair_text.lower()
            except AttributeError:
                pass
        return False

    def post_is_free(self, post):
        if self.always_free:
            return True
        elif self.re_free:
            return self.re_free.search(post.title.lower())
        return False

    def search(self, keywords):
        return self.controller.search(keywords)
