#!/usr/bin/python

#
# written by @eric_capuano
# https://github.com/ecapuano/web-traffic-generator
#
# published under MIT license :) do what you want.
#

# 20170714 shyft ADDED python 2.7 and 3.x compatibility and generic config
# 20200225 rarawls ADDED recursive, depth-first browsing, color stdout
# 20200617 svenvanhal Thesis-specific updates.
from __future__ import print_function

import random
import re
import requests
import signal
import sys
import time
from os import environ
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def signal_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

try:
    import config
except ImportError:

    class ConfigClass:  # minimal config incase you don't have the config.py
        MAX_DEPTH = 10  # dive no deeper than this for each root URL
        MIN_DEPTH = 3  # dive at least this deep into each root URL
        MAX_WAIT = 10  # maximum amount of time to wait between HTTP requests
        MIN_WAIT = 5  # minimum amount of time allowed between HTTP requests
        DEBUG = False  # set to True to enable useful console output

        # use this single item list to test how a site responds to this crawler
        # be sure to comment out the list below it.
        # ROOT_URLS = ["https://digg.com/"]
        ROOT_URLS = [
            "https://www.reddit.com"
        ]

        # items can be a URL "https://t.co" or simple string to check for "amazon"
        blacklist = [
            'facebook.com',
            'pinterest.com'
        ]

        # must use a valid user agent or sites will hate you
        USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'


    config = ConfigClass


def make_driver():
    # Define selenium webdriver
    options = Options()
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument(f'user-agent={config.USER_AGENT}')

    proxy = environ.get('http_proxy')
    if proxy is not None:

        options.add_argument(f'--proxy-server={proxy}')

        print(f"Using proxy: {proxy}")

        desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        desired_capabilities['proxy'] = {
            "httpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
            'noProxy': '',
            'class': "org.openqa.selenium.Proxy",
            'autodetect': False
        }
        driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)

    else:
        print(f"Using NO proxy")
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(30)
    return driver


class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    NONE = '\033[0m'


def debug_print(message, color=Colors.NONE):
    """ A method which prints if DEBUG is set """
    if config.DEBUG:
        print(color + message + Colors.NONE)


def hr_bytes(bytes_, suffix='B', si=False):
    """ A method providing a more legible byte format """

    bits = 1024.0 if si else 1000.0

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes_) < bits:
            return "{:.1f}{}{}".format(bytes_, unit, suffix)
        bytes_ /= bits
    return "{:.1f}{}{}".format(bytes_, 'Y', suffix)


def do_request(url):
    """ A method which loads a page """

    debug_print("  Requesting page...".format(url))
    driver = make_driver()

    try:

        try:
            last_log = driver.get_log('browser')[-1]['message']
        except:
            last_log = ""

        start_time = time.time()
        driver.get(url)
        debug_print(f"  Last log line: {last_log}")
        debug_print(f"  Page source:")
        debug_print(driver.page_source[:255])
        debug_print(f"  Loading time: {time.time() - start_time:.1f}s")

        # Get links
        links = []
        elems = driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                links.append(href)

        driver.quit()

        return links

    except Exception as e:
        print(e)
        driver.quit()
        return False


def get_links(page):
    """ A method which returns all links from page, less blacklisted links """

    pattern = r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
    links = re.findall(pattern, str(page.content))
    valid_links = [link for link in links if not any(
        b in link for b in config.blacklist)]
    return valid_links


def recursive_browse(url, depth):
    """ A method which recursively browses URLs, using given depth """
    # Base: load current page and return
    # Recursively: load page, pick random link and browse with decremented depth

    debug_print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    debug_print(
        "Recursively browsing [{}] ~~~ [depth = {}]".format(url, depth))

    if not depth:  # base case: depth of zero, load page

        do_request(url)
        sleep_time = random.randrange(config.MIN_WAIT, config.MAX_WAIT)
        debug_print("  Pausing for {} seconds...".format(sleep_time))
        time.sleep(sleep_time)
        return

    else:  # recursive case: load page, browse random link, decrement depth

        valid_links = do_request(url)  # load current page

        # give up if error loading page
        if valid_links is False:
            debug_print(
                "  Stopping and blacklisting: page error".format(url), Colors.YELLOW)
            config.blacklist.append(url)
            sleep_time = random.randrange(config.MIN_WAIT, config.MAX_WAIT)
            debug_print("  Pausing for {} seconds...".format(sleep_time))
            time.sleep(sleep_time)
            return

        # give up if no links to browse
        if not valid_links:
            debug_print("  Stopping and blacklisting: no links".format(
                url), Colors.YELLOW)
            config.blacklist.append(url)
            sleep_time = random.randrange(config.MIN_WAIT, config.MAX_WAIT)
            debug_print("  Pausing for {} seconds...".format(sleep_time))
            time.sleep(sleep_time)
            return

        # sleep and then recursively browse
        sleep_time = random.randrange(config.MIN_WAIT, config.MAX_WAIT)
        debug_print("  Pausing for {} seconds...".format(sleep_time))
        time.sleep(sleep_time)

        recursive_browse(random.choice(valid_links), depth - 1)


if __name__ == "__main__":

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Traffic generator started")
    print("https://github.com/ecapuano/web-traffic-generator")
    print("Diving between 3 and {} links deep into {} root URLs,".format(
        config.MAX_DEPTH, len(config.ROOT_URLS)))
    print("Waiting between {} and {} seconds between requests. ".format(
        config.MIN_WAIT, config.MAX_WAIT))
    print("This script will run indefinitely. Ctrl+C to stop.")

    while True:
        debug_print("Randomly selecting one of {} Root URLs".format(
            len(config.ROOT_URLS)), Colors.PURPLE)

        random_url = random.choice(config.ROOT_URLS)
        depth = random.choice(range(config.MIN_DEPTH, config.MAX_DEPTH))

        recursive_browse(random_url, depth)

