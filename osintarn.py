#!/usr/bin/python3

import requests
import argparse
import re
import urllib.parse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='osintarn')
parser.add_argument('--domain','-d',help='domain')
parser.add_argument('--verbose','-v',type=bool,default=False,help='verbose')
args = parser.parse_args()

domain = args.domain
verbose = args.verbose

def _skymem():
	burp0_url = "https://www.skymem.info:443/srch?q=%s" % domain
	response = requests.get(burp0_url)
	emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text)
	domain_ids = re.findall(r'<a href="/domain/([a-z0-9]+)\?p=', str(response.text))
	previoussize = 0
	for i in range(1,20):
		burp0_url = "https://www.skymem.info/domain/%s?p=%s" % ("".join(domain_ids),i)
		response = requests.get(burp0_url)
		if previoussize == len(response.content):
			break
		emails.extend(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text))
		emails = sorted(set(emails))
		previoussize = len(response.content)
	#print('\n'.join(emails))
	result = []
	for i in emails:
		if domain in i: result.append(i)
	return result

def _emailcrawlr():
	burp0_url = "https://emailcrawlr.com:443/api/domain_test?domain=%s" % domain
	response = requests.get(burp0_url)
	emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text)
	emails = sorted(set(emails))
	#print("".join(emails))
	result = []
	for i in emails:
		if domain in i: result.append(i)
	return result

def _crawl():
	#urls = ['http://search.yahoo.com/search?p=%22%40{}%22&n=100&start=1".format(domain)']
	#urls = ['https://www.bing.com/search?q="%40{}"'.format(domain)]
	urls = ['https://{}'.format(domain)]
	#urls = ['https://www.google.com/search?num=100&start=0&hl=en&q=%22%40{}%22'.format(domain)]
	for url in urls:
		response = requests.get(url)
		emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text)
		links = get_links(url)
		print("[+] Number of links to crawl:", len(links))
		for link in links:
			try:
				if verbose: print("[+] parsing:", link)
				response = requests.get(link)
				emails.extend(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text))
			except:
				pass
	result = []
	for i in emails:
		if domain in i: result.append(i)
	return(result)

def get_links(url):
	urls = set()
	soup = BeautifulSoup(requests.get(url).text, "html.parser")
	for a in soup.findAll("a"):
		link = a.attrs.get("href")
		link = urllib.parse.urljoin(url, link)
		if is_valid_url(link):
			urls.add(link)
	return list(urls)

def is_valid_url(url):
    parsed = urllib.parse.urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and (parsed.scheme == "http" or parsed.scheme == "https")




result = []
result.extend(_skymem())
result.extend(_emailcrawlr())
result.extend(_crawl())

result = sorted(set(result))
print('\n'.join(result))
print("[+] emails:", len(result))
