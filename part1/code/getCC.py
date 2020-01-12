import requests
import argparse
import time
import json
from io import BytesIO
import gzip
import csv
import codecs
from urllib.parse import urlencode
from bs4 import BeautifulSoup

# Arguments parsing
ap = argparse.ArgumentParser()
ap.add_argument("-d","--domain",required=True,help="The domain to target ie. cnn.com")
args = ap.parse_known_args()[0]
domain = args.domain

index_list = ["2019-04","2019-09","2019-13"]

# Searches domain
def search_domain(domain):
    record_list = []  
    for index in index_list:
        cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain
        
        response = requests.get(cc_url)
        if response.status_code == 200:
            records = response.content.splitlines()
            for record in records:
                record_list.append(json.loads(record))

    return record_list        

# Downloads from Common Crawl
def download_page(record):

    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1

    prefix = 'https://commoncrawl.s3.amazonaws.com/'
    url = prefix + record['filename']
    headers = {'Range': 'bytes={}-{}'.format(offset, offset_end)}
    ccresponse = requests.get(url, headers=headers)
    rawdata = BytesIO(ccresponse.content)
    f = gzip.GzipFile(fileobj=rawdata)
    data = f.read()
    data = str(data, encoding = "utf-8", errors='ignore')
    response = ""
    
    if len(data):
        try:
            warc, header, response = data.strip().split('\r\n\r\n', 2)
        except:
            pass
            
    return response

# Extract links 
def extract_external_links(html_content,link_list):
    parser = BeautifulSoup(html_content)
    links = parser.find_all("a")
    if links:
        for link in links:
            href = link.attrs.get("href")
            if href is not None:
                if domain not in href:
                    if href not in link_list and href.startswith("http"):
                        link_list.append(href)
    return link_list

record_list = search_domain(domain)
link_list   = []

for record in record_list:
    html_content = download_page(record)
    link_list = extract_external_links(html_content,link_list)

with codecs.open("%s-links.csv" % domain,"wb",encoding="utf-8") as output:
    fields = ["URL"]
    logger = csv.DictWriter(output,fieldnames=fields)
    logger.writeheader()
    for link in link_list:
        logger.writerow({"URL":link})