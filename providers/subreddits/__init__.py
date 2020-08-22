from abc import ABC
import praw
from freebie import Freebie
from credentials import reddit_api as secrets

REDDIT = praw.Reddit(
    client_id=secrets['client_id'],
    client_secret=secrets['client_secret'],
    user_agent=secrets['user_agent'],
    username=secrets['username'],
    password=secrets['password']
)


class Subreddit(ABC):
    def __init__(self, subreddit, provider_name=None, always_free=False):
        self.controller = REDDIT.subreddit(subreddit)
        self.provider_name = f"/r/{subreddit}"
        self.always_free = always_free
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
        if posts is None:
            posts = self.get_posts(sort_by="new", limit=limit)
        for post in posts:
            match_free = None
            if not self.always_free:
                match_free = self.re_free.search(post.title.lower())
            match_title = self.re_title.search(post.title)
            match_platform = self.re_platform.search(post.title)
            if (self.always_free or match_free) and match_title:
                this_post = Freebie(
                    title=match_title.group(0),
                    url=post.url,
                    provider=f"{self.provider_name} ({post.shortlink})"
                )
                if match_platform:
                    this_post.platform = match_platform.group(0)
                freebies.append(this_post)
        return freebies

    def search(self, keywords):
        return self.controller.search(keywords)
