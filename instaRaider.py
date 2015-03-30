#!/usr/bin/env python
"""
instaRaider.py

This function contains code that is originally Copyright (c) {{{2014}}} {{{Amir Kurtovic}}}

This code is a modified version of: https://github.com/akurtovic/InstaRaider

the original code is not working well with new instagram website design
Original modification was made on 03/06/2015

"""
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import re
from time import sleep
import urllib
import urllib2
import os
import sys
import argparse
import pdb
import requests

class instaRaider(object):

    def getImageCount(self, url):
        '''
        Given a url to Instagram profile, return number of photos posted
        '''
        response = urllib2.urlopen(url)
        countsCode = re.search(r'counts\":{\"media\":\d+', response.read())
        count = re.findall(r'\d+', countsCode.group())
        return int(count[0])

    def URLexists(self,url):
        r = requests.head(url)
        return r.status_code == requests.codes.ok


    def loadInstagram(self, profileUrl):
        '''
        Using Selenium WebDriver, load Instagram page to get page source
    
        '''
        count = self.getImageCount(self.profileUrl)
        print self.userName + " has " + str(count) + " photos on Instagram."

        print "Loading Selenium WebDriver..."
        
        # Load webdriver and scale window down
        driver = webdriver.Firefox()
        driver.set_window_size(200,200)
        driver.set_window_position(100,100)

        print "Loading Instagram profile..."
        # load Instagram profile and wait for PAUSE 
        driver.get(self.profileUrl)
        driver.implicitly_wait(self.PAUSE)

        # Check if the profile is private. If so, exit
        try:
            driver.find_element_by_css_selector('.MediaComp')
        except:
            sys.exit("User profile is private. Aborting.")

        clicks = (int(count)-60)/20+1

        for x in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sys.stdout.write('.')
            sys.stdout.flush()
            sleep(self.PAUSE)
    
        #pdb.set_trace()
        # Load full Instagram profile if more than initial 60 photos desired
        if (args.count < 61):
            pass
        else:
            # Click on "Load more..." label
            ##pdb.set_trace()
            ## seems not working
            ##element = driver.find_element_by_xpath(self.loadLabelXPATH)
            ## new
            element = driver.find_element_by_class_name('PhotoGridMoreButton')

            for y in range(clicks):
                #print(y)
                element.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sys.stdout.write('.')
                sys.stdout.flush()
                sleep(self.PAUSE)
     
        # After load all profile photos, return source to getPhotos()
        source = BeautifulSoup(driver.page_source)
        
        # close Firefox window
        driver.close()

        return source

    def validUser(self, userName):
        '''
        returns True if Instagram username is valid
        '''
        # check if Instagram username is valid
        req = urllib2.Request(self.profileUrl)

        try:
            urllib2.urlopen(req)
        except:
            return False
        # if req doesn't fail, user profile exists
        return True

    def photoExists(self, url):
        '''
        Returns true if photo exists
        Used when checking which suffix Instagram used for full-res photo
        url: URL to Instagram photo
        '''
        try:
            urllib2.urlopen(url)
        except:
            return False
    
        return True


    def getPhotos(self, source, userName, count):
        '''
        Given source code for loaded Instagram page,
        extract all hrefs and download full-resolution photos
    
        source: HTML source code of Instagram profile papge
        '''
        # directory where photos will be saved
        directory = './Images/' + userName + '/'

        # check if directory exists, if not, make it
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # logfile to store urls is csv format
        logfile = './Images/' + userName + '/' + userName + '.csv'
        try:
            file = open(logfile, "a")
        except IOError:
            print "\nLog file does not exist."

        # photo number for file names
        photoNumber = 0
    
        # indexes for progress bar
        photosSaved = 0
        progressBar = 0

    
        print "\nRaiding Instagram..."
        print "Saving photos to " + directory
    
        print "------"
        # print progress bar
        print "Photos saved so far:"
        print "---------10--------20--------30--------40--------50"

        ##pdb.set_trace()
        for x in source.findAll('div', {'class':'Image'}):
            if (photoNumber >= count):
                break
            else:
                # increment photonumber for next image
                photoNumber += 1
            
                #extract url to thumbnail from each photo
                ##x = x.div
                ##rawUrl = x['style']
                ##cgao
                rawUrl = x['src']
                # rawUrl is the thumbnail url
                # for photos after 2014:
                #   I need to remove '/s306x306/e15' from it
                # https://scontent.cdninstagram.com/hphotos-xap1/t51.2885-15/s306x306/e15/10683944_526319734180228_164050056_n.jpg
                # for photos before 2014?
                #   I need to change trailing '6.jpg' to '7.jpg'
                # https://scontent.cdninstagram.com/hphotos-xpf1/outbound-distilleryimage6/t0.0-17/OBPTH/378c229620b511e3bdd322000ae90d23_6.jpg
                # for some, I need to change trailing '6.jpg' to '8.jpg'
                #https://scontent.cdninstagram.com/hphotos-xfa1/outbound-distilleryimage1/t0.0-17/OBPTH/60e6518ab40211e3b686124d53b510cd_6.jpg    

                ##photoUrl = rawUrl[21:-2]
                ##cgao

                #convert from unicode to ASCII
                rawUrl = rawUrl.encode('utf-8')
                if '/s306x306/e15' in rawUrl:
                    photoUrl = rawUrl.replace('/s306x306/e15','')   
                    print(userName + " " + str(count) + " " + str(photoNumber) + ": scheme 1")
                elif 'outbound-distilleryimage' in rawUrl:
                    photoUrl = rawUrl.replace('6.jpg','7.jpg')
                    if(not self.URLexists(photoUrl)):
                        photoUrl = rawUrl.replace('6.jpg','8.jpg')
                    print(userName + " " + str(count) + " " + str(photoNumber) + ": scheme 2")
                    print(rawUrl)
                    print(photoUrl)
                else:
                    #print(photoNumber, ": not valid url: ",rawUrl)
                    #photoNumber -= 1
                    #continue #skip current loop step.
                    print(userName + " " + str(count) + " " + str(photoNumber) + ": probably a thumbnail image: ")
                    print(rawUrl)    
                    photoUrl = rawUrl     
                #if photoNumber < 329:
                #    continue

                photoName = directory + userName + "_" + str(photoNumber) + '.jpg'
                #print(photoNumber, photoUrl)
                # save full-resolution photo
                urllib.urlretrieve(photoUrl, photoName)
                
                # save filename and url to CSV file
                file.write(photoUrl + "," + photoName + "\n")
            
                # print hash to progress bar
                if (photosSaved == 50):
                    photosSaved = 1
                    progressBar += 50
                    sys.stdout.write('\n')
                    sys.stdout.write('#')
                    sys.stdout.flush()
                
                else:
                    # increment progress bar
                    photosSaved += 1
                    sys.stdout.write('#')
                    sys.stdout.flush()
                
                sleep(self.PAUSE)

        print "\n------"
        print "Saved " + str(photoNumber) + " images to " + directory
        
        # close logfile
        file.close()
        print "Saved activity in logfile: " + logfile
    
    
    def __init__(self, userName):
        self.userName = userName
        self.profileUrl = 'http://instagram.com/' + userName + '/'
        self.PAUSE = 1
        self.loadLabelXPATH = "/html/body/div/div/div/section/div/span/a/span[2]/span/span"

if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser(description="InstaRaider")
    parser.add_argument('-u', '--user', help="Instagram username", required=True)
    parser.add_argument('-c', '--count', help="# of photos to download", type=int)
    args = parser.parse_args()

    if (args.user):
        userName = args.user

        raider = instaRaider(userName)
        url = raider.profileUrl

        if(raider.validUser(userName)):

            if not args.count:
                count = raider.getImageCount(url)
                args.count = count
            else:
                count = args.count
                if raider.getImageCount(url) < count:
                    print "You want to dowload %r photos." % args.count
                    print "The user only has %r photo." % raider.getImageCount(url)
                    print "Downloading all photos."
                    count = raider.getImageCount(url)
                    args.count = count
            
            # Get source code from fully loaded Instagram profile page
            source = raider.loadInstagram(url)

            # Download all photos identified on profile page
            raider.getPhotos(source, userName, count)
        else:
            print "Username " + userName + " is not valid."
        