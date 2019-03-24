# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:04:22 2019

@author: johns
"""

import requests
import urllib.request
import time, os
from bs4 import BeautifulSoup
import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

os.chdir('C:/Users/johns/Documents/Courtney Dad Blog Text')

#To start we want to create a list that links to every post.
#We start with the main url and then tack on page numbers
#(the first for loop). Next we search for all header1 with a
#class of entry-title.  We loop through that result for each page
#grabbing the link.
url = 'http://myahalifestyle.com/index.php/page/'
response = requests.get(url)
post_urls = []
for i in range(1,5):
    #this connects us to a specific page
    response = requests.get(url+str(i))
    page = BeautifulSoup(response.text, 'html.parser' )
    links = page.findAll('h2', {'class':'entry-title'})
    for j in range(0, len(links)):
        post=links[j].find('a')
        link = post['href']
        post_urls.append(link)
        
        
posts=pd.DataFrame(columns = ['URL', 'Title', 'Post'])

#Now that we have a list of all of the links, we call each one
#in the loop. We grab the title and the text, then
#append them to our dataframe
for i in range(0,len(post_urls)):
    site = post_urls[i]
    newresponse = requests.get(site)
    post = BeautifulSoup(newresponse.text, 'html.parser')
    
    title = post.findAll(class_ = 'entry-title')
    title = title[0].text.strip()

    text = post.findAll(class_ = 'entry-content')
    text = text[0].text.strip()
    text = text.replace('\n\n\n', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    new_entry = [site, title, text]
    posts.loc[i] = new_entry


document = Document()
for i in range(0, len(posts['Post Number'])):
    
 
    title_text = str(posts.Title[i])
    document.add_heading(title_text, level =1)
    

    paragraph = document.add_paragraph()
    paragraph.add_run(posts.Post[i])
    
document.save('my aha lifestyle.docx')