# -*- coding: UTF-8 -*-

# @package KeepUp
# @author ma11
# @brief Application to help keeping stuff up to date
# @details It provides program which stores tags in a file with timestamp
#   The program can update the timestamps to current time, print every tags and timestamp, or print only tags which timestamp are older than a given period of time.

from optparse import OptionParser
from time import time,ctime

# Usefull snippet from http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
# to replace line in a file
from tempfile import mkstemp
from shutil import move
from os import remove, close

def convertToTs(duration):
    dur=duration
    mapping={'s':'*1+','m':'*60+','h':'*3600+','d':'*86400+','w':'*604800+','M':'*2592000+','Y':'*31536000+'}
    for k,v in mapping.iteritems():
        dur=dur.replace(k,v)
    dur=dur[:-1]
    return eval(dur)
             
# @class Item
# @brief Represent an item to keep udated
# @detail An item hold a tag and a timestamp.
# It has methods to test wether the timestamp is older than a given duration
class Item():
    # @brief The tag name
    tag = ''

    # @biref The timestamp of the tag
    timestamp = 0.0 

    def __init__(self,tag,ts=time()):
        self.tag = tag
        self.timestamp = float(ts)

    ## Return true if item is older than the given duration (ie. it it is older than 1 week)
    # @param duration A string representing the duration. For example, a duration of one day two hours three minutes would be '1d2h3m'
    def isOlderThan(self,duration):
        return self.timestamp < (time() - convertToTs(duration))


# @class App
# @brief Hold application methods
class App():
    # @brief The filename which contains the tags and timestamps
    filename = 'tags.txt'

    def __init__(self,*args,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

    ## Read the file self.filename and extract lines
    def getLinesFromFile(self):
        try:
            with open(self.filename,'r') as f:
                lines=f.readlines()
        except IOError:
            print "Error: can't open file "+self.filename+". If the file does not existing start by adding an item first."
            lines=()
        return lines

    ## A usefull function to replace a pattern in file self.filename (see http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python)
    # @detail It create a new temporary file, copy and replace line after line, and move the temporary file in the place of self.filename
    # @param pattern The string to replace
    # @param subst The string pattern is to be replaced by
    def replace(self, pattern, subst):
        #Create temp file
        fh, abs_path = mkstemp()
        with open(abs_path,'w') as new_file:
            with open(self.filename) as old_file:
                for line in old_file:
                    new_file.write(line.replace(pattern, subst))
        close(fh)
        #Remove original file
        remove(self.filename)
        #Move new file
        move(abs_path, self.filename)

    ## Return a list of Item() elements stored in self.filename
    def getItemsFromFile(self):
        lines=self.getLinesFromFile()
        return [  Item(li.split(',')[0],li.split(',')[1]) for li in lines]

    ## Print the list of items contained in file self.filename
    def printList(self):
        its = self.getItemsFromFile()
        for it in its:
            print '{0:10} | {1:10}'.format(it.tag, ctime(it.timestamp))

    ## Create a new Item() element with current timestamp.
    # @param name New item's name
    def newItem(self,name):
        with open(self.filename,'a') as fname:
            fname.write(name+','+str(time())+','+'\n')

    ## Print only items older than a given duration
    # @param duration The duration items are supposed to be older than. For instance, duration older than one month and two days is written '1M2d'
    def extractOlderThan(self,duration):
        its = self.getItemsFromFile()
        ito = [ it for it in its if it.isOlderThan(duration) ]

        for it in ito:
            print '{0:10} | {1:10}'.format(it.tag, ctime(it.timestamp))

    ## Update timestamp of an item
    # @param item Tag of the item to be updated
    def updateItem(self,items):
        lines=self.getLinesFromFile()
        itemList = items.split(',')
        for it in itemList:
            for li in lines:
                elem = li.split(',')
                if elem[0]==it:
                    self.replace(elem[0]+','+elem[1],elem[0]+','+str(time()))
                    break

    ## Runtime of the application
    def main(self):
	    optparser = OptionParser(version='%prog '+str(self.version))

            optparser.add_option("-a","--add",help="Add a new ITEM to the list", default='',dest="newItem", metavar="ITEM")
            optparser.add_option("-u","--update",help="Update ITEM in the list", default='',dest="updateItem", metavar="ITEM")
            optparser.add_option("-f","--file",help="Use FILE to store the instead of default location", default=self.filename,dest="filename", metavar="FILE")
            optparser.add_option("-l","--list",help="List all items to keep updated",action="store_true",default="false", dest="printList")
            optparser.add_option("-o","--older-than",help="Extract items older than DURATION",metavar="DURATION",default="",dest='duration')

	    (options, args) = optparser.parse_args()
            self.filename = options.filename

            if options.printList == True:
                self.printList()

            if not options.newItem == '':
                self.newItem(options.newItem)

            if not options.duration == '':
                self.extractOlderThan(options.duration)

            if not options.updateItem == '':
                self.updateItem(options.updateItem)

if __name__ == '__main__':
    app=App(version='alpha',filename='tutu')
    app.main()
