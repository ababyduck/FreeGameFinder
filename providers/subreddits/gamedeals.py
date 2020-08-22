import re
import freebie
from providers.subreddits import Subreddit

RE_TITLE = re.compile(r"(?<=] ).+(?= \()")
RE_PLATFORM = re.compile(r"(?<=\[).+(?=])")
RE_FREE = re.compile(r"(?<=\().*100% off|-100%|\$0\.00.*(?=\))")
# todo read settings file for platforms to exclude, e.g. itch.io


class GameDeals(Subreddit):
    def __init__(self):
        super().__init__(subreddit="gamedeals")

    def get_freebies(self, limit=100):
        freebies = []
        for post in self.get_posts(sort_by="new", limit=limit):
            if RE_FREE.search(post.title.lower()):
                freebies.append(freebie.Freebie(
                    title=RE_TITLE.search(post.title).group(0),
                    url=post.url,
                    provider=self.provider_name,
                    platform=RE_PLATFORM.search(post.title).group(0),
                ))
        return freebies

