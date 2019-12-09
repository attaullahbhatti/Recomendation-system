from flask import Flask , render_template , request, url_for, redirect
import functions
import csv
import re
server=Flask(__name__)

@server.route("/")
def main():
    movieFound = 0
    return render_template('index.html',movieFound=movieFound)

@server.route("/sendbyGet/<movieName>", methods=['GET'])
def sendbyGet(movieName):
    movieFound = 1
    #Part One:Getting Entered Movie's Data
    with open('final.csv',encoding="UTF8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[7]==movieName:
                standardMovie = functions.Superclean(row)
                movieFound +=1
                break
    #End Of Part One
    if movieFound==1:
        return render_template('index.html',movieFound=movieFound)
    moviesList = functions.KNN(standardMovie)
    return render_template('results.html',movie=standardMovie,moviesList=moviesList)


@server.route("/send", methods=['POST'])
def send():
    movieFound = 1
    movieName = request.form['name']
    #Part One:Getting Entered Movie's Data
    with open('final.csv',encoding="UTF8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[7]==movieName:
                standardMovie = functions.Superclean(row)
                movieFound +=1
                break
    #End Of Part One
    if movieFound==1:
        return render_template('index.html',movieFound=movieFound)
    moviesList = functions.KNN(standardMovie)
    return render_template('results.html',movie=standardMovie,moviesList=moviesList)

if __name__=="__main__":
    server.run()
    
    