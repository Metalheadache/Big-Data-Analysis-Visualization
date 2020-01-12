# Long running time
# Get content from urls

import json
import io
import sys
import csv
from newsplease import NewsPlease

with open('health-links.csv','r',encoding='utf-8') as articlefile:
    reader = csv.reader(articlefile)
    rows = list(reader)
    articleStored = []
    
    for i in range(1, len(rows)-1):
        try:
            url = ''.join(rows[i])
            article = NewsPlease.from_url(url)
        except:
            pass
        if not article.text:
            i = i+1
        else:
            articleStored.append(article.text.replace('\n', ''))

        with open('./CCarticles_1.csv', 'w', newline='\n', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(articleStored)

articlefile.close()