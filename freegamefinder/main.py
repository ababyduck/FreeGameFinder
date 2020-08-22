from .providers.subreddits import gamedeals as rgd
from .providers.subreddits import freegamefindings as rfgf

# todo check database of deals
# todo check known sources for new deals (cron?)
# todo report new deals on discord
# todo implement web interface
# web interface should include scoring, removing false positives, blocking sources (i.e. subreddits user)
# todo implement epic, prime, humble, gog giveaway, uplay, etc


def test_reddit():
    r_gamedeals = rgd.GameDeals()
    for freebie in r_gamedeals.get_freebies():
        print(freebie, "\n")

    r_freegamefindings = rfgf.FreeGameFindings()
    for freebie in r_freegamefindings.get_freebies():
        print(freebie, "\n")


if __name__ == '__main__':
    test_reddit()