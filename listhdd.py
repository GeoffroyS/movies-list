#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

#-------------------------------------
#  /!\ check libxml2 is installed /!\
# todo: - series!
#       - refactor, rewrite isFile/main
#       - test runtime imdbpie v imdbpy
#       - PDF
#       - add .avi
#-------------------------------------

import os
import magic
import math
import re
import guessit
import imdb
from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
from pyPDF2 import PdfFileWriter, PdfFileReader

#----------------------Classes
class Movie:
    def __init__(self, title, date = 1):
        self.title = title
        self.date = date
        self.URL = 'url'
        
class Series:
    def __init__(self, title):
        self.title = title
        self.URL = 'url'
  
  
#----------------------Functions        
def isMovie(file):
    fileFormat = magic.from_file(file)
    if 'Matroska data' in fileFormat or 'MP4' in fileFormat:
        movie = True
    else:
        movie = False
    return movie    
    
def realName(filename):
    guess = guessit.guess_movie_info(filename)
    realFileName = guess['title']
    return realFileName
    
def date(filename): 
    guess = guessit.guess_movie_info(filename)
    date = guess['year']
    return date 
     
def isFile(moviesList, seriesList, directory):
    i = 0
    for file in os.listdir(directory):
        pathfile=directory+'/'+file
        if os.path.isfile(pathfile) == True: #FILE
            if isMovie(pathfile) == True:
                
                filename = os.path.basename(file) # file name with dots, quality, team...
                realFileName = realName(filename) # 'proper' movie name
                
                if (not re.search(r"(.*)[ .]S(\d{1,2})E(\d{1,2})", filename)) == True: # if not series:
                    dateMovie = date(filename)  # movie year
                    movieInstance = Movie(realFileName, dateMovie) # creation of a 'Movie' instance
                    moviesList.append(movieInstance) # appends this instance to the list
                    resultIMDb = fetchInstance(realFileName, dateMovie) # fetching from IMDb
                    movieInstance.rating = resultIMDb['rating']
                    movieInstance.url = resultIMDb['cover url']
                    movieInstance.plot = resultIMDb['plot']
                    
                else: # Series!
                    seriesInstance = Series(realFileName)
                    seriesList.append(seriesInstance)
                    #match = re.findall(r"(.*)[ .]S(\d{1,2})E(\d{1,2})", filename) # part of the string matched
                    fetchInstance(realFileName)
                
                i += 1
        else: # recursive call for folders
            isFile(moviesList, seriesList, pathfile) 
    return moviesList, seriesList
    
def displayMoviesList(moviesList):    
    for i in xrange(0, len(moviesList)):    
        print 'movie title: ', moviesList[i].title
        print 'movie date: ', moviesList[i].date
        print 'cover url: ', moviesList[i].url
        print 'movie rating: ', moviesList[i].rating, '\n'
        
def displaySeriesList(seriesList):
    for i in xrange(0, len(seriesList)):    
        print 'series title: ', seriesList[i].title, '\n'
        
def fetchInstance(realFileName, dateMovie = 0):
    imdb_access = imdb.IMDb()
    if dateMovie != 0:
        titleDate = realFileName + ' ' + str(dateMovie)
        resultIMDb = imdb_access.search_movie(titleDate)[0]
        imdb_access.update(resultIMDb) # retrieve useful information
#        print 'imdbpy fetch result                ', resultIMDb.summary(), '\n'
        
    else: # SERIES TO DOOOOOOOOOOOOOOOOO
        resultIMDb = realFileName
        
    return resultIMDb
        
def main(path = ''):
    Tk().withdraw() # no full GUI: keeps the root window from appearing
    if path == '':
        directory = askdirectory()
    else:
        directory = path
        
    moviesList = [] 
    seriesList = []   
    isFile(moviesList, seriesList, directory)
    
    displayMoviesList(moviesList)
    displaySeriesList(seriesList)


if __name__ == "__main__":
    main()
    
    