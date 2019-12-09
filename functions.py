from flask import Flask , render_template , request, url_for, redirect
import json
import math
import re
import csv


def Superclean(movie):
    listofGenres = []
    listofSpokenLanguages = []
    listofProdComp = []
    posterPath=""
    movieData = {"genres":"","overview":"","popularity":"","poster_path":"","production_companies":"","release_date":"","spoken_languages":"","title":"","vote_average":""}

    match = re.findall(r'\'([^\']*)\'', movie[0])
    for item in match:
        listofGenres.append(item)

    posterPath = 'https://image.tmdb.org/t/p/original'+movie[3]

    match = re.findall(r'\'([^\']*)\'', movie[6])
    for item in match:
        listofSpokenLanguages.append(item)
 
    match = re.findall(r'\'([^\']*)\'', movie[4])
    for item in match:
        listofProdComp.append(item)
    
    movieData['genres'] = listofGenres
    movieData['overview'] = movie[1]
    movieData['popularity'] = movie[2]
    movieData['poster_path'] = posterPath
    movieData['title'] = movie[7]
    movieData['vote_average'] = movie[8]
    movieData['release_date'] = movie[5]
    movieData['spoken_languages'] = listofSpokenLanguages
    movieData['production_companies'] = listofProdComp

    return movieData

def KNN(standardMovie):
    sortedMoviesList = []
    movieDistance = []

    with open("final.csv",encoding="UTF8") as csv_file:
        moviesList = csv.reader(csv_file, delimiter=',')
        next(moviesList, None)
        for movie in moviesList:
            movie = Superclean(movie)
            if(movie['title']!=standardMovie['title']):
                movieDistance=[]
                euclideanDistance = 0

# popularity
                standardPopularity = float(standardMovie['popularity'])
                neighbourPopularity = float(movie['popularity'])
                popularityDifference = standardPopularity - neighbourPopularity
                popularity = pow( popularityDifference,2)
# RElease Date
                standardreleaseDate = float(standardMovie['release_date'])
                neighbourreleaseDate = float(movie['release_date'])
                releaseDateDifference = standardreleaseDate - neighbourreleaseDate
                releaseDate = pow(releaseDateDifference,2)
# rating
                standardrating = float(standardMovie['vote_average'])
                neighbourrating = float(movie['vote_average'])
                ratingDifference = standardrating -neighbourrating
                rating = pow(ratingDifference,2)
# considering title also as by google in priority
                neighbourMovie = movie['title'].split(" ") #split string into a list
                stdMovie = standardMovie['title'].split(" ")  
                l=len(neighbourMovie)
                l1=len(stdMovie)
                if (l<l1):
                    for i in range(l):
                        if stdMovie[i]==neighbourMovie[i]:
                            euclideanDistance-=100
                if (l1<l):
                    for i in range(l1):
                        if stdMovie[i]==neighbourMovie[i]:
                            euclideanDistance-=100
 # genres cosidering                       

                for genre in movie['genres']:
                    for standardGenre in standardMovie['genres']:
                        if genre!=standardGenre:
                           euclideanDistance+=30
 # production_companies cosidering                  
                for company in movie['production_companies']:
                    for standardProdComp in standardMovie['production_companies']:
                        if company==standardProdComp:
                            euclideanDistance=euclideanDistance - 100
# spoken_languages cosidering                
                for language in movie['spoken_languages']:
                    for standardLanguage in standardMovie['spoken_languages']:
                        if language!=standardLanguage:
                            euclideanDistance+=1

                euclideanDistance =  euclideanDistance + popularity + (releaseDate) + (rating)
                #euclideanDistance = math.sqrt(euclideanDistance)
                movieDistance.append(euclideanDistance)
                movieDistance.append(movie['title'])
                movieDistance.append(movie['poster_path'])
                sortedMoviesList.append(movieDistance)

    sortedMoviesList = sorted(sortedMoviesList, key=lambda x: x[0])
    return sortedMoviesList

    

