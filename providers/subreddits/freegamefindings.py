import re
import freebie
from providers.subreddits import Subreddit


class FreeGameFindings(Subreddit):
    def __init__(self):
        super().__init__(subreddit="freegamefindings")
