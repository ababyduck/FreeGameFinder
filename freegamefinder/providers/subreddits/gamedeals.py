import re
from freegamefinder.providers.subreddits import Subreddit


class GameDeals(Subreddit):
    # https://www.reddit.com/r/GameDeals/
    def __init__(self, limit: int = 100):
        super().__init__(subreddit="GameDeals", limit=limit)
        self.re_free = re.compile(r"(?<=\().*100% off|-100%|\$0\.00.*(?=\))")
        self.re_title = re.compile(r"(?<=] ).+(?= \()")
        self.re_platform = re.compile(r"(?<=\[).+(?=])")
