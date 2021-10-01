import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect
import random

def scrapIt(url):
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')

    anchors = soup.find_all("option")
    allLinks = []
    linkDict = {}
    for link in anchors:
        if(link['value']):
            ls = []
            str = link['value']
            if(str == 'combine-tags-by-or'):
                continue
            ls.append(str)
            if(str.find(" ") > 0):
                str = str.replace(" ", "%20")
            ls.append(str)
            linkUrl = "http://codeforces.com/problemset?tags=" + str
            linkDict[str] = linkUrl
            allLinks.append(ls)
    return linkDict,allLinks

url = "http://codeforces.com/problemset#"



app = Flask(__name__)
linkDict,allLinks = scrapIt(url)

def problemScrap(url):
    
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    div = soup.find_all("td", {"class": "id"})
    problems = []
    for x in div:
        anchor = x.find("a")
        plink = "https://codeforces.com" + anchor['href']
        problems.append(plink)
    return problems


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        topic = request.form['topic']
        ques = problemScrap(linkDict[topic])
        q1 = random.randint(0,len(ques)-1)
        q2 = random.randint(0,len(ques)-1)
        while(q2 == q1):
            q2 = random.randint(0,len(ques))
        problems = [ques[q1], ques[q2]]
        qTopic = topic.replace("%20"," ")
        return render_template('index.html', linkDict=linkDict,allLinks=allLinks, problems=problems, qTopic=qTopic)
    return render_template('index.html', linkDict=linkDict,allLinks=allLinks)
    


if __name__ == "__main__":
    app.run(debug=True, port=8000)
