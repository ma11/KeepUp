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


# @class App
# @brief Hold application methods
class App():
    # @brief The filename which contains the tags and timestamps
    filename = 'tags.txt'

    def __init__(self,*args,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

    def getLinesFromFile(self):
        try:
            with open(self.filename,'r') as f:
                lines=f.readlines()
                f.close()
        except IOError:
            print "Error: can't open file "+self.filename+". If the file does not existing start by adding an item first."
            lines=()
        return lines

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

    def convertToTs(self,duration):
        dur=duration
        mapping={'s':'*1+','m':'*60+','h':'*3600+','d':'*86400+','w':'*604800+','M':'*2592000+','Y':'*31536000+'}
        for k,v in mapping.iteritems():
            dur=dur.replace(k,v)
        dur=dur[:-1]
        return eval(dur)
             

    def printList(self):
        lines=self.getLinesFromFile()
        for li in lines:
            elem = li.split(',')
            print elem[0] +'   --   '+ctime(float(elem[1]))

    def newItem(self,name):
        with open(self.filename,'a') as fname:
            fname.write(name+','+str(time())+','+'\n')
            fname.close()

    def extractOlderThan(self,duration):
        ts = self.convertToTs(duration)
        limit = time() - ts
        lines=self.getLinesFromFile()
        for li in lines:
            elem = li.split(',')
            if float(elem[1])<limit:
                print elem[0]+'   --   '+ctime(float(elem[1])) 

    def updateItem(self,items):
        lines=self.getLinesFromFile()
        itemList = items.split(',')
        for it in itemList:
            for li in lines:
                elem = li.split(',')
                if elem[0]==it:
                    self.replace(elem[0]+','+elem[1],elem[0]+','+str(time()))
                    break

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
