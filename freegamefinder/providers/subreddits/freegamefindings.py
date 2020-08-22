import re
from freegamefinder.providers.subreddits import Subreddit


class FreeGameFindings(Subreddit):
    # https://www.reddit.com/r/FreeGameFindings/
    def __init__(self, limit: int = 100):
        super().__init__(subreddit="FreeGameFindings", limit=limit, always_free=True, expired_flair="expired")
        self.re_title = re.compile(r"(?<=\) )[^(]+")
        self.re_platform = re.compile(r"(?<=\[).+(?=])")
        self.re_category = re.compile(r"(?<=\()[^(]+(?=\))")

    def get_freebies(self):
        filtered_posts = []
        posts = self.get_posts(sort_by="new")
        for post in posts:
            try:
                category = self.re_category.search(post.title).group(0).lower()
            except AttributeError:
                continue
            if category == "game":
                filtered_posts.append(post)
        return super().get_freebies(posts=filtered_posts)
