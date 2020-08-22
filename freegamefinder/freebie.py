from datetime import datetime, timezone


TIME_FORMAT = "%b %d %Y %I:%M %p (UTC%z)"


class Freebie:
    def __init__(self, title, url, provider, discovered=None, platform=None, starts=None, expires=None):
        self.title = title
        self.url = url
        self.provider = provider
        self.platform = platform
        self.starts = starts
        self.expires = expires
        if discovered is None:
            self.discovered = datetime.now(timezone.utc)
        else:
            self.discovered = discovered

    def __str__(self):
        basic_info = f"{self.title}\n" \
                     f"{self.url}\n" \
                     f"Source: {self.provider}\n" \
                     f"Discovered: {self.discovered.astimezone().strftime(TIME_FORMAT)}"
        if self.expires:
            return f"{basic_info}\nExpires: {self.expires}"
        return basic_info
