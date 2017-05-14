#!/usr/bin/python

#this script assumes that the plants are all adequately watered as a starting state.
#make sure all probes have both LEDs lit.

import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import time # This is the time library, we need this so we can use the sleep function
import tweepy #contains the twitter functions
import pandas as pd #allows dataframes
import numpy as np #allows groovy math with dataframes
from datetime import datetime as dt #allows time functions for determining when the script loops
import picamera

global camera
camera=picamera.PiCamera()
global array_length
array_length=5



def select_message(veg,veg_status):
    #import .csv file as a dataframe
    df = pd.read_csv('messages3.csv',delimiter=",",encoding="utf-8-sig")
    df=df.reset_index()
    
    #filter the dataframe down to a single message
    df2 = df[(df['veg'] == veg)]
    df2 = df[(df['veg'] == veg)]
    df3 = df2[(df2['status'] == veg_status)]
    df3.take(np.random.permutation(len(df3))[:1])
    df4=df3.take(np.random.permutation(len(df3))[:1])
    #package up the message
    message = veg +": "+ df4.iloc[0,3]
    print(message)
    tweeter(message)
              


def tweet_photo(message):
    
    # Consumer keys and access tokens, used for OAuth
    consumer_key = "31cVEnEldpc6lOTrw1UFa7a5W"
    consumer_secret = "KqEBo7avJLFoygeCsEzNFuf2lWGlfuxsULcfsIwAg4gvewt2dh"
    access_token = "851110327886336000-JfnTRTLhxO0cXoZGDAG4oUBxjcMRzXm"
    access_token_secret = "vfjEJZabNY7d1EhxPqkG36cBZ67vd2fwNsSmKoFAHCDM4"

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)

    # Send the tweet with photo
    camera.capture('image1.jpg') #takes the picture
    photo_path = 'image1.jpg'
    status = message +"\n"+ dt.now().strftime('%Y/%m/%d %H:%M:%S')
            
    try:
        print('attempting photo tweet')
        api.update_with_media(photo_path, status=status)
        print('photo tweet successful')
        
    except:
        print('tweet unsuccessful')
    
            
    


#function that tweets moisture status
def tweeter(message):
    
    # Consumer keys and access tokens, used for OAuth
    consumer_key = "31cVEnEldpc6lOTrw1UFa7a5W"
    consumer_secret = "KqEBo7avJLFoygeCsEzNFuf2lWGlfuxsULcfsIwAg4gvewt2dh"
    access_token = "851110327886336000-JfnTRTLhxO0cXoZGDAG4oUBxjcMRzXm"
    access_token_secret = "vfjEJZabNY7d1EhxPqkG36cBZ67vd2fwNsSmKoFAHCDM4"

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    
    tweet = message + "\n"+dt.now().strftime('%Y/%m/%d %H:%M:%S')
        
    try:
        print('attempting tweet')
        status = api.update_status(status=tweet)
        print('tweet successful')
        
    except:
        print('tweet failed')
            
    

def check_state():
    current_state=[]
    #store the current pin states in a list
    for i in range(array_length):
        pin_val=GPIO.input(channels[i])
        current_state.extend(str(pin_val))

    for i in range(array_length):
        current_state[i]=int(current_state[i])
    return(current_state)

def compare_states(current_state,previous_state):
    
    for i in range(array_length):
        if (current_state[i]==fine_df.iloc[i,2] and previous_state[i]!=fine_df.iloc[i,2]):
            veg=fine_df.iloc[i,1]
            print(veg)
            state='fine'
            select_message(veg,state)
        elif current_state[i] == fine_df.iloc[i,2]:
            pass
        else:
            veg=fine_df.iloc[i,1]
            state='need'
            select_message(veg,state)
    return

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins that we have our digital output from our sensor connected to
channels = [17,5,26,15,21]



# Set the GPIO pins to input mode
for each in channels:
        GPIO.setup(each, GPIO.IN)

#create a dataframe that correlates a "fine" state to a pin status (1 or 0)
fine_df=pd.DataFrame({"pin":channels,"veg":['cabbage','beans','radishes','lettuce','carrots']})
fine_df["state"]=""

for i in range(array_length):
    fine_df["state"][i]=GPIO.input(channels[i])

#declares penultimate state and gives it initial values    
previous_state=check_state()        
current_state=check_state()

try:
    
    while True:
        print(dt.now().strftime('%Y/%m/%d %H:%M:%S'))

        if dt(dt.now().year,dt.now().month,dt.now().day,8) < dt.now() < dt(dt.now().year,dt.now().month,dt.now().day,16):
            print('checking...')
            previous_state=current_state
            current_state=check_state()
            compare_states(current_state,previous_state)
            print('done checking')
            
        if dt(dt.now().year,dt.now().month,dt.now().day,8) < dt.now() < dt(dt.now().year,dt.now().month,dt.now().day,9):
            print('morning tweet')
            message="Good Morning!"
            tweet_photo(message)
            print('done morning tweet')
                             
        if dt(dt.now().year,dt.now().month,dt.now().day,16) < dt.now() < dt(dt.now().year,dt.now().month,dt.now().day,17):
            print('evening tweet')
            message="Good Night!\n"
            tweet_photo(message)
            print('done evening tweet')
        
          
        time.sleep(3600)
        
        
    
        
except KeyboardInterrupt:
    print("Script Aborted:Happy Now?")

#except:
    #print("Other Error or Exception Occurred")

finally:
    GPIO.cleanup()



