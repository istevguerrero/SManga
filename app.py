from flask import Flask, render_template, redirect
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

@app.route("/downloadManga/<mangaName>/<chapterNumber>/<int:pageNumber>", methods=["GET"])

def downloadManga(mangaName, chapterNumber, pageNumber):

    mangaURL = "https://mangahub.io/manga/" + mangaName

    chapterListURLArray = getChapterList(mangaURL, mangaName)

    chapterImagesURLArray = getIndividualChapterImagesArray(chapterListURLArray, mangaName, chapterNumber)

    chapterImage = chapterImagesURLArray[pageNumber]

    chapterImageNext = chapterImagesURLArray[pageNumber + 1]

    if(pageNumber > 1):

        chapterImagePrevious = chapterImagesURLArray[pageNumber - 1]

    else:

        chapterImagePrevious = "#"

    return render_template("reader.html", chapterImage = chapterImage , chapterImageNext = chapterImageNext, chapterImagePrevious = chapterImagePrevious)


def getChapterList(mangaURL, mangaName):

    response = requests.get(mangaURL)

    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all("a")

    chapterListURLArray = []

    for image in images:

        imageHref = str(image.get("href"))

        if( "https://mangahub.io/chapter/" + mangaName + "/chapter-" in imageHref):

            chapterListURLArray.append(str(image.get("href")))

    return chapterListURLArray.reverse()

def getIndividualChapterImagesArray(chapterListURLArray, mangaName, chapterNumber):

    scraper = cloudscraper.create_scraper()

    response = scraper.post("https://api.mghubcdn.com/graphql", data={"query":"{chapter(x:m01,slug:\"" + mangaName + "\",number:" + chapterNumber + "){id,title,mangaID,number,slug,date,pages,noAd,manga{id,title,slug,mainSlug,author,isWebtoon,isYaoi,isPorn,isSoftPorn,unauthFile,isLicensed}}}"})

    soup = json.loads(response.text)

    chapterImagesURLArray = []

    for imageCode in (json.loads(soup["data"]["chapter"]["pages"])).values():

        chapterImagesURLArray.append("https://img.mghubcdn.com/file/imghub/" + imageCode)

    print(chapterImagesURLArray)

    return chapterImagesURLArray


if(__name__ == "__main__"):

    app.run(debug=True)