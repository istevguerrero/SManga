from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


import requests
from bs4 import BeautifulSoup
import cloudscraper
import json

app = Flask(__name__)

app.config["SQALCHEMY_DATABASE_URI"] = "SQLITE:///database/info.db"

db = SQLAlchemy(app)

@app.route("/")

def home():

    return render_template("index.html")

@app.route("/manga")

def manga():

    return render_template("apartamento.html")

@app.route("/downloadManga")

def downloadManga():

    mangaCode = "vagabond_119"

    chapterSeedUrl = "https://mangahub.io/manga/" + mangaCode

    chapterListArray = getChapterList(chapterSeedUrl, mangaCode)

    getIndividualChapterImagesArray(chapterListArray, 0)

    return "Welcome"


def getChapterList(chapterSeedUrl, mangaCode):

    response = requests.get(chapterSeedUrl)

    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all("a")

    chapterListArray = []

    for image in images:

        imageHref = str(image.get("href"))

        if( "https://mangahub.io/chapter/" + mangaCode + "/chapter-" in imageHref):

            chapterListArray.append(str(image.get("href")))

    return chapterListArray.reverse()

def getIndividualChapterImagesArray(chapterListArray, chapterNumber):

    scraper = cloudscraper.create_scraper()

    response = scraper.post("https://api.mghubcdn.com/graphql", data={"query":"{chapter(x:m01,slug:\"vagabond_119\",number:1){id,title,mangaID,number,slug,date,pages,noAd,manga{id,title,slug,mainSlug,author,isWebtoon,isYaoi,isPorn,isSoftPorn,unauthFile,isLicensed}}}"})

    soup = json.loads(response.text)

    imageCodeArray = []

    for imageCode in (json.loads(soup["data"]["chapter"]["pages"])).values():

        imageCodeArray.append(imageCode)

    imageURL = "https://img.mghubcdn.com/file/imghub/" + imageCodeArray[0]

    print(imageURL)

    return "hola"

    



    

if(__name__ == "__main__"):

    app.run(debug=True)