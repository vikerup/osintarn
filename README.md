# osintarn

## Gettings started

`osintarn.py` is a python script used to gather email addresses for a company by way of open source intelligence (OSINT).

The script was developed to quickly get a hand-full of email addresses that could be used in either credential stuffing 
attacks or phishing campaigns during authorized penetration tests and red team exercises.

## How it works

The scripts starts by scraping https://www.skymem.info for emails addresses followed by https://emailcrawlr.com. No API keys are required.
This is followed up by crawling all URLs that exists on the targetted company's main webpage while scraping for email addresses. 
Lastly the scripts scrapes PGP keyserver for email addresses.

## Usage

`python3 osintarn.py --domain test.tld`

## Credits

Inspiration from https://github.com/smicallef/spiderfoot
