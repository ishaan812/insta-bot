import os
from flask.helpers import url_for
from instagramy.plugins.download import *
from flask import Flask, request,send_file
from flask.templating import render_template
from instagramy import *
import urllib.request
import instaloader
from instaloader.structures import *
from werkzeug.utils import redirect
urllist=list()



session_id='472395887%3Ai7sh95Ef2iTbDd%3A19'

app = Flask(__name__)

@app.route('/')
def usernameform():
    return render_template("profilebot.html")

@app.route('/result',methods=["GET","POST"])
def result():
    if request.method == 'POST':
        username=request.form['username']
        user=InstagramUser(username,sessionid=session_id)
        profilepictureurl=user.profile_picture_url
        fullname=user.fullname
        privatebool=user.is_private
        no_of_posts=user.number_of_posts
        link=user.website
        bio=user.biography
        followernumber=user.number_of_followers
        followingnumber=user.number_of_followings
        urllib.request.urlretrieve(profilepictureurl, "static/dptemp.jpeg")
        return render_template("results.html",name=fullname,followercount=followernumber,followingcount=followingnumber,bio=bio,postnumber=no_of_posts,link=link,priv_bool=privatebool,username=username )

@app.route('/postsloading/<username>',methods=["GET","POST"])
def postsloading(username):
    username=username
    loader=instaloader.Instaloader()
    loader.login("testpy812","hibye123")
    i=0
    profile=Profile.from_username(loader.context,username)
    posts=profile.get_posts()
    for post in posts:
        i+=1
        urllist.append(post.url)
    return redirect(url_for('posts',username=username,pagenumber=1))
    
@app.route('/posts/<username>/<pagenumber>',methods=["GET","POST"])
def posts(username,pagenumber):
    postpagenumber=int(pagenumber)
    username=username
    postnumber=len(urllist)
    start=(postpagenumber-1)*9
    for i in range(start,start+9):
        if i>=postnumber: 
            #if os.path.exists("static/posts/temppost%s.jpeg"%i):
             #   os.remove("static/posts/temppost%s.jpeg"%i)
            break
        urllib.request.urlretrieve(urllist[i], "static/posts/temppost%s.jpeg"%(i-start))
    return render_template("posts.html",start=start,postnumber=postnumber,pagenumber=postpagenumber,username=username)

@app.route('/download_profile_picture',methods=["GET","POST"])
def downloaddp():
    return send_file("/py/py4e/instabot_website/static/dptemp.jpeg", as_attachment=True)
    

@app.route('/download_post/<postnumber>',methods=["GET","POST"])
def downloadpost(postnumber):
    file_location=("/py/py4e/instabot_website/static/posts/temppost"+str(postnumber)+".jpeg")
    return send_file(file_location,as_attachment=True)


            



   
if __name__ == '__main__':
   app.run(debug=True)     