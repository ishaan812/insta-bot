import instaloader
from instaloader.structures import *
from os import name
from instagramy.plugins.download import *
from flask import Flask, request,send_file
from flask.templating import render_template
from instagramy import *
import urllib.request
import instaloader
from instaloader.structures import *

urllist=list()
postpagenumber=1
loader=instaloader.Instaloader()
username="kanyewest"
profile=Profile.from_username(loader.context,username)
posts=profile.get_posts_data()
for post in posts:
    urllist.append(post)
print(urllist)



