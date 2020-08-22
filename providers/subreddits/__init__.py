import praw
from credentials import reddit_api as secrets

REDDIT = praw.Reddit(
    client_id=secrets['client_id'],
    client_secret=secrets['client_secret'],
    user_agent=secrets['user_agent'],
    username=secrets['username'],
    password=secrets['password']
)


class Subreddit:
    def __init__(self, subreddit, provider_name=None):
        self.controller = REDDIT.subreddit(subreddit)
        self.provider_name = f"/r/{subreddit}"

    def get_posts(self, sort_by="new", limit=100):
        if sort_by == "new":
            return self.controller.new(limit=limit)
        elif sort_by == "top":
            return self.controller.top(limit=limit)
        elif sort_by == "hot":
            return self.controller.hot(limit=limit)
        return None

    def get_freebies(self, limit):
        raise NotImplemented
