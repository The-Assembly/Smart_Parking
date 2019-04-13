#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522       
import signal
import time

continue_reading = True
# the uid of the last recognized card
lastcarduid = None
# the time a card uid was last seen
lastcardtime = 0.0

UsersIn = []

lastCards = []

# this long after a card has been noticed, it can be noticed again
# This works because the reader generates repeated notifications of the card
# as it is held agains the reader - faster than this interval.
# The timer is restarted every time the reader generates a uid.
# If you sometimes get repeated new card IDs when holding a card against the
# reader, increase this a little bit.
CARDTIMEOUT = 1.0

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

## Welcome message
#print "Welcome to the MFRC522 data read example"
#print "Press Ctrl-C to stop."

def getUser(userid):
    return "test"

def checkTime():
    seconds = time.time()
    local_time = time.ctime(seconds)
    char="\\\""
    local_time = char+local_time+char
    return local_time
    
def gettypename( typecode ):
    typecode &= 0x7F;
    if typecode == 0x00:
        return "MIFARE Ultralight or Ultralight C"
    elif typecode == 0x01:
        return "MIFARE TNP3XXX"
    elif typecode == 0x04:
        return "SAK indicates UID is not complete"
    elif typecode == 0x08:
        return "MIFARE 1KB"
    elif typecode == 0x09:    
        return "MIFARE Mini, 320 bytes"
    elif typecode == 0x10 or typecode == 0x11:
        return "MIFARE Plus"
    elif typecode == 0x18:
        return "MIFARE 4KB"
    elif typecode == 0x20:
        return "PICC compliant with ISO/IEC 14443-4"
    elif typecode == 0x40:
        return "PICC compliant with ISO/IEC 18092 (NFC)"
    return "Unknown type";

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        
    # Get the UID of the card
    (status,rawuid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:
        uid = "{0[0]:02x}{0[1]:02x}{0[2]:02x}{0[3]:02x}".format(rawuid)
#        print "Card read UID: "+uid
        newcard = False
        if uid in lastCards:
            User = getUser(uid)
            UsersIn.remove(User)
            newcard = False
        else:
            newcard = True
            
        if newcard:

            rawcardtype = MIFAREReader.MFRC522_SelectTag(rawuid)
            cardtypename = gettypename( rawcardtype )
            timein = checkTime()
            User = getUser(uid)
            UsersIn.append(User)
            lastCards.append(uid)
            
        if User in UsersIn:
            status = "\\\"1\\\""
            print '{ "User":"'+uid+'","Time":"'+timein+'","Checked":"'+status+'" }'
            time.sleep(2)
        
        elif User not in UsersIn:
            timeout = checkTime()
            status = "\\\"0\\\""
            print '{ "User":"'+uid+'","Time":"'+timeout+'","Checked":"'+status+'" }'
            lastCards.remove(uid)
            time.sleep(2)
        #if newcard == False:
            #User = getUser()
            #UsersIn.remove(User)
        # remember the last card uid recognized
        lastcarduid = uid
        # remember when it was seen
        lastcardtime = time.clock()

