import re
from providers.subreddits import Subreddit


class FreeGameFindings(Subreddit):
    # https://www.reddit.com/r/FreeGameFindings/
    def __init__(self):
        super().__init__(subreddit="FreeGameFindings", always_free=True)
        self.re_title = re.compile(r"(?<=\) )[^(]+")
        self.re_platform = re.compile(r"(?<=\[).+(?=])")
        self.re_category = re.compile(r"(?<=\()[^(]+(?=\))")

    def get_freebies(self, limit=100):
        filtered_posts = []
        posts = self.get_posts(sort_by="new", limit=limit)
        for post in posts:
            try:
                expired = post.link_flair_text.lower() == "expired"
                category = self.re_category.search(post.title).group(0).lower()
            except AttributeError:
                continue
            if not expired and category == "game":
                filtered_posts.append(post)
        return super().get_freebies(posts=filtered_posts)
