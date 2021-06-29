from flask import redirect, render_template, Flask, request, url_for, send_file
from bs4 import BeautifulSoup
from html import escape
import json, re, ssl, smtplib, requests, random, os, datetime
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote
from base64 import b64encode
from pathlib import Path
import json, datetime, requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def sendmail(receiver,subject,text,html="NOT INPUT BY USER."):

    mailhost = 'smtp.zoho.com'
    mailid = 'noreply@intellx.co.in'
    mailps = 'Keepguessing200#'

    if html == "NOT INPUT BY USER.":
        html = render_template("email.html",
                               mail = receiver,
                               message = text,
                               subject = subject)

    sender_email = mailid
    receiver_email = receiver
    password = mailps
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    server = smtplib.SMTP('smtp.zoho.com:587')
    server.starttls()
    server.login(mailid,password)
    server.sendmail(mailid, receiver_email, message.as_string())
    server.quit()

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():

    var = {
            "title" : "about",
            "paragraph" : {
                            "title" : "aaditya rengarajan.",
                            "content" : '''hello! i am aadityarengarajan,
a freelancer, and i am profecient in web development.
i know HTML5, CSS3, Bootstrap, Material Design, MDB, Python,
Flask, discord.py, VB.NET, batch, bash, arduino/c++, javascript,
a bit of COBOL and a bit of kotlin.'''
                          },
            "button" : {
                          "title" : "available for work ('hire')",
                          "link"  : url_for('hire')
                       }
          }

    return render_template("paragraph.html", var = var)

@app.route('/work/music')
def work_music():

    var = {
            "title" : "work/music",
            "paragraph" : {
                            "title" : "deepblu.",
                            "content" : '''deepblu. is a gulf-based orchestral/R&B/trap
record producer. Having expressed an interest for beat-making in his early teens and aiming
to redefine music, deepblu. draws inspiration from artists like Aaryan Shah, 12AM, The Weeknd,
Johnny Rain, sobhhÏ, pre kai ro, Black Atlass, Drake and Bridge.'''
                          },
            "button" : {
                          "title" : "see my music ('blu')",
                          "link"  : "http://blu.intellx.co.in/"
                       }
          }

    return render_template("paragraph.html", var = var)

@app.route('/work/programming')
def work_programming():

    with open("projects.json") as projects_file:
        projects = json.load(projects_file)

    monthly = [0,0,0,0,0,0,0,0,0,0,0,0]
    times={}
    for project in projects:
        date = int((datetime.datetime.strptime(project["code"].split('-')[1],"%d%m%Y")).strftime("%m"))
        monthly[date-1] += 1
        time = int(str(int(round((int(str(project["code"].split('-')[2][:2]))+int(str(project["code"].split('-')[2][2:4]))/60),0))))
        if time not in times:
            times.update({time:1})
        else:
            times.update({time:times[time]+1})
    
    thismonth = monthly[int(datetime.datetime.now().strftime("%m"))]

    var = {
            "title" : "work/programming",
            "projects" : projects,
            "month" : thismonth
          }

    return render_template("carousel.html", var = var)

@app.route('/work/aviation')
def work_aviation():

    var = {
            "title" : "work/aviation"
          }

    response = app.response_class(
        response=render_template("carousel.html", var = var),
        mimetype='text/html'
      )

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/hire', methods=["GET","POST"])
def hire():

    if request.method=="GET":

        var = {
                "title" : "work"
              }

        return render_template("hire-me.html", var = var)

    else:

        sendmail(request.form.get("E-mail"),"[aadityarengarajan] received request","thank you, we have received your request and will get back to you via e-mail ASAP.")


        sendmail("aadit.xo@gmail.com","[aadityarengarajan] request for project",json.dumps(request.form,indent=4))

        return redirect(url_for("index"))


if __name__=="__main__":
    app.run(
        debug=True,
        use_reloader=True,
        use_debugger=True,
        port=5000,
        host='0.0.0.0',
        use_evalex=True,
        threaded=True,
        passthrough_errors=False
        )