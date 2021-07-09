MAX_DEPTH = 8  # maximum click depth
MIN_DEPTH = 2  # minimum click depth
MAX_WAIT = 15  # maximum amount of time to wait between HTTP requests
MIN_WAIT = 5  # minimum amount of time allowed between HTTP requests
DEBUG = True  # set to True to enable useful console output

# use this single item list to test how a site responds to this crawler
# be sure to comment out the list below it.
# ROOT_URLS = ["https://www.tudelft.nl"]

ROOT_URLS = [
    "https://www.tudelft.nl/",
    "https://www.nos.nl",
    "https://www.nu.nl",
    "https://www.tweakers.net/",
    "https://www.ah.nl",
    "https://www.jumbo.com",
    "https://www.marktplaats.nl",
    "https://nl.wikipedia.org/wiki/Main_Page",
    "https://www.reddit.com",
    "https://www.youtube.com",
    "https://www.funda.nl",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.buienradar.nl",
    "https://unix.stackexchange.com/questions/",
]

# items can be a URL "https://t.co" or simple string to check for "amazon"
blacklist = [
    "https://t.co",
    "t.umblr.com",
    "messenger.com",
    "itunes.apple.com",
    "l.facebook.com",
    "bit.ly",
    "mediawiki",
    ".css",
    ".ico",
    ".xml",
    "intent/tweet",
    "twitter.com/share",
    "signup",
    "login",
    "dialog/feed?",
    ".png",
    ".jpg",
    ".json",
    ".svg",
    ".gif",
    "zendesk",
    "clickserve",
    "api.whatsapp",
    "/?hl=",
    "mailto:"
]

# must use a valid user agent or sites will hate you
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
