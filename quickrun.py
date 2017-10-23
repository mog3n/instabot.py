
#--------------------------------------------------------
'''
This file is intended for non-programmers for quick 
access to the tool.

Simply fill in the details below and run the python 
file (by typing into CMD or Terminal 'python quickrun.py')
without the quotes.

'''

# Enter the Instagram username and password for the account
cred_username       = "" # Your username here
cred_password       = "" # Your password here

# Settings

# General
likes_per_minute            = 30 # Enter the amount of post likes per minute
follows_per_minute          = 1 # Enter amount of accounts to follow per minute
minutes_until_unfollow      = 60 # Enter amount of time until the bot unfollows that account (60 = 1 hour)
auto_comments_per_hour      = 30 # Amount of comments per hour

# Hashtags
hashtags_to_like            = [ # Photos with these hashtags will be liked (randomly)
                                    'follow4follow','fashion','cute'
                              ] 

hashtags_to_ignore          = [ # Photos with these haghtags will be ignored
                                    'rain', 'thunderstorm'
                              ] 

# Comments (Advanced)
# Essentially, selected phrases will randomize to create one sentence.

comments_to_post = [
                                
                                [   # First phrase
                                    "this", "the", "your"
                                ],

                                [   # Second phrase
                                    "photo", "picture", "pic", "shot", "snapshot"
                                ],

                                [   # Third phrase
                                    "is", "looks", "feels", "is really"
                                ],

                                [   # Fourth phrase
                                    "great", "super", "good", "very good", "good", "wow",
                                    "WOW", "cool", "GREAT","magnificent", "magical",
                                    "very cool", "stylish", "beautiful", "so beautiful",
                                    "so stylish", "so professional", "lovely",
                                    "so lovely", "very lovely", "glorious","so glorious",
                                    "very glorious", "adorable", "excellent", "amazing"
                                ],

                                [   # Fifth phrase
                                    ".", "..", "...", "!", "!!", "!!!"
                                ] 

]


# That's it! Run by typing 'python /my_directory/quickrun.py'


#--------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], 'src'))

from check_status import check_status
from feed_scanner import feed_scanner
from follow_protocol import follow_protocol
from instabot import InstaBot
from unfollow_protocol import unfollow_protocol

bot = InstaBot(
    login=cred_username,
    password=cred_password,
    like_per_day=likes_per_minute*60*24,
    comments_per_day=auto_comments_per_hour*60*24,
    tag_list=hashtags_to_like,
    tag_blacklist=hashtags_to_ignore,
    user_blacklist={},
    max_like_for_one_tag=50,
    follow_per_day=follows_per_minute*60*24,
    follow_time=minutes_until_unfollow,
    unfollow_per_day=follows_per_minute*60*24,
    unfollow_break_min=15,
    unfollow_break_max=30,
    log_mod=0,
    proxy='',
    # List of list of words, each of which will be used to generate comment
    # For example: "This shot feels wow!"
    comment_list=[["this", "the", "your"],
                  ["photo", "picture", "pic", "shot", "snapshot"],
                  ["is", "looks", "feels", "is really"],
                  ["great", "super", "good", "very good", "good", "wow",
                   "WOW", "cool", "GREAT","magnificent", "magical",
                   "very cool", "stylish", "beautiful", "so beautiful",
                   "so stylish", "so professional", "lovely",
                   "so lovely", "very lovely", "glorious","so glorious",
                   "very glorious", "adorable", "excellent", "amazing"],
                  [".", "..", "...", "!", "!!", "!!!"]],
    # Use unwanted_username_list to block usernames containing a string
    ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
    ### 'free_followers' will be blocked because it contains 'free'
    unwanted_username_list=[
        'second', 'stuff', 'art', 'project', 'love', 'life', 'food', 'blog',
        'free', 'keren', 'photo', 'graphy', 'indo', 'travel', 'art', 'shop',
        'store', 'sex', 'toko', 'jual', 'online', 'murah', 'jam', 'kaos',
        'case', 'baju', 'fashion', 'corp', 'tas', 'butik', 'grosir', 'karpet',
        'sosis', 'salon', 'skin', 'care', 'cloth', 'tech', 'rental', 'kamera',
        'beauty', 'express', 'kredit', 'collection', 'impor', 'preloved',
        'follow', 'follower', 'gain', '.id', '_id', 'bags'
    ],
    unfollow_whitelist=['example_user_1', 'example_user_2'])
while True:

    #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
    #print("## MODE 1 = MODIFIED MODE BY KEMONG")
    #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
    #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
    #print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
    #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

    ################################
    ##  WARNING   ###
    ################################

    # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
    ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

    mode = 0

    #print("You choose mode : %i" %(mode))
    #print("CTRL + C to cancel this operation or wait 30 seconds to start")
    #time.sleep(30)

    if mode == 0:
        bot.new_auto_mod()

    elif mode == 1:
        check_status(bot)
        while bot.self_following - bot.self_follower > 200:
            unfollow_protocol(bot)
            time.sleep(10 * 60)
            check_status(bot)
        while bot.self_following - bot.self_follower < 400:
            while len(bot.user_info_list) < 50:
                feed_scanner(bot)
                time.sleep(5 * 60)
                follow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)

    elif mode == 2:
        bot.bot_mode = 1
        bot.new_auto_mod()

    elif mode == 3:
        unfollow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 4:
        feed_scanner(bot)
        time.sleep(60)
        follow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 5:
        bot.bot_mode = 2
        unfollow_protocol(bot)

    else:
        print("Wrong mode!")
