# For a GUI, better performance, more functions, and easiness to use... Check out: www.unisoftdev.tech

'''
* @ Twitter explorer
* Created By: Juraj Vysvader
* Author's profile: https://www.linkedin.com/in/jurajvysvader
                    https://www.linkedin.com/company/unisoftdev 
* Creation date: 10.3.2019
* Business website: https://www.unisoftdev.tech
* @license http://www.gnu.org/copyleft/lgpl.html GNU/GPL
* @Copyright (C) 2019 Juraj Vysvader. All rights reserved.
'''


#! /usr/bin/python


import tweepy, json, datetime, time, re, random, json
from time import sleep
from re import search
from itertools import cycle
from random import shuffle, randint
import string
from json import loads
from datetime import date
import history



# gets all of our data from the config file.
with open('assets/config.json', 'r') as config_file:
    config_data = json.load(config_file)

screen_name = config_data["auth"]["screen_name"]

# authorization from values inputted earlier, do not change.
auth = tweepy.OAuthHandler(config_data["auth"]["CONSUMER_KEY"], config_data["auth"]["CONSUMER_SECRET"])
auth.set_access_token(config_data["auth"]["ACCESS_TOKEN"], config_data["auth"]["ACCESS_SECRET"])
api = tweepy.API(auth)


count = 0
starting_point = 0
keywords_balance = 1

################
daily_limit = 30 # <----------  change this number of maximal amount of sent replies per day 
################

contacted_users = [] # one reply per one user
keywords_size = int(len(config_data["keywords_questions"]))


def random_break_time():
    random_sleep_time = randint(121, 439) # set up the number of seconds that the bot is sleeping
    sleep(random_sleep_time)

def deep_sleep():
    first_randomized = randint(6, 13) # set up the number of hours to sleep
    second_randomized = randint(1, 60) # set up the number of additional minutes
    first_step = 60 * 60 * first_randomized
    second_step = second_randomized * 60 
    third_step = first_step + second_step
    sleep(third_step)

# customize your function to handle errors
def error_handling(e):
    error = type(e)
    if error == tweepy.RateLimitError:
        print("You've hit a limit! Sleeping.")
        deep_sleep()
    if error == tweepy.TweepError:
        print('Uh oh. Could not complete task. Sleeping.')
        random_break_time()
    else:
        print('error... Could not complete task. Sleeping.')
        random_break_time()


def add_contact(user):
    contacted_users.append(user)


ndata = ''

                
def restart():
    print('hibernating')
    global count 
    global keywords_size
    global daily_limit
    global starting_point
    global keywords_size
    global ndata
    global keywords_balance
    ndata = ''
    count = 0
    contacted_users[:] = []
    keywords_size = 0
    import variables
    variables.unisoftdev_new_tweet = 0
    variables.daily_limit = daily_limit
    keywords_size = int(len(config_data["keywords_questions"]))
    deep_sleep()
    if str(date.today()) not in variables.date:
        variables.date = str(date.today())
        variables.sql_daily_limit = 0
        starting_point = 2 
        keywords_balance = 1
    start()              


def day(the_current_day, daily_limit):
    import variables
    variables.daily_limit = daily_limit
    variables.date = the_current_day

def twitterbot_loads_tweets():
    global ndata
    global daily_limit
    convert_message = ndata
    message = convert_message['text']
    tweetID = convert_message['tweetID']
    user_name = convert_message['user_name']

    ##################################################################################################################################
    # Variations... Some people think they can win in Lotto (and easily). 
    # I don't think it's a big chance, so I let you use the regex:
    ##################################################################################################################################
    
    # 9 times increases the probability of a match
    exchangable_verbs = ["want", "wanna", "need", "look", "search", "discover", "seek", "wish", "desire"]
    for need_verbs in exchangable_verbs:
        message = message.replace(need_verbs, "@verbs")
        
    # 8 x 9 = 72 times increases the probability of a match if both are used
    exchangable_questions = ["how", "what", "what", "is there", "are there", "does", "where", "is this"]
    for how in exchangable_questions:
        message = message.replace(how, "@questions")
        
    # 15 x 8 x 9 = 1080 times increases the probability of a match if all 3 are used
    exchangable_nouns = ["php developer", "python developer", "django developer", "web developer", "webdeveloper", "anyone", "freelancer", "freelance", "sysadmin", "web-developer", "web developer", "developer", "designer", "php programmer", "php coder"]
    for who in exchangable_nouns:
        message = message.replace(who, "@nouns")   

    greetings_list = ["hi! ", "hi, ", "hi! ", "hello! ", "hiya! ", "hey! ", "nice to meet you. ", "good to see you. ", "glad to see you. ", "it's my pleasure to meet you. "]
    greetings = random.choice(greetings_list)

    answer_one = ["That's good to read from you. PM?", "Can you provide some details, PM?", "Can you check with me?", "I'm here.", "Coming...", "Please, get in touch, email@example.com"]
    first_answer = random.choice(answer_one)

    answer_two = ["Welcome, how can I help you?", "Hello, thanks for your message. How are you?", "Welcome inwards, a team member will be soon in touch"]
    second_answer = random.choice(answer_two)

    answer_three = ["twitterbot@example.com", "01010101 Bot Street"]
    third_answer = random.choice(answer_three)

    user_name = user_name.replace('"', '')


    if user_name not in contacted_users:
        global daily_limit
        global starting_point
        the_current_day = str(date.today()) 
        twitter_user_name = user_name
        if re.match(r'(.*)I @verbs a( remote | )@nouns(.*)', message): ### <-------- change regular expressions, pattern matching
            import variables
            if starting_point < 2:
                day(the_current_day, daily_limit)
            history.database(twitter_user_name, the_current_day)
            if variables.sql_daily_limit < daily_limit:
                if variables.unisoftdev_new_tweet > 0:
                    variables.unisoftdev_new_tweet = 0
                    print('tweet sent')
                    add_contact(user_name)
                    api.update_status('@'+str(user_name)+' '+greetings+first_answer, tweetID)
                    random_break_time()
            else:
                print(variables.sql_daily_limit)
                print(daily_limit)
                restart()
        elif re.match(r'(.*)hello twitter bot(.*)', message): ### <-------- change regular expressions, pattern matching
            import variables
            if starting_point < 2:
                day(the_current_day, daily_limit)
            variables.daily_limit = daily_limit
            history.database(twitter_user_name, the_current_day)
            if variables.sql_daily_limit < daily_limit:
                if variables.unisoftdev_new_tweet > 0:
                    variables.unisoftdev_new_tweet = 0
                    print('tweet sent')
                    add_contact(user_name)
                    api.update_status('@'+str(user_name)+' '+greetings+second_answer, tweetID)
                    random_break_time()
            else:
                restart()
        elif re.match(r'(.*)Twitter bot(.*)contact(.*)', message): ### <-------- change regular expressions, pattern matching
            import variables
            if starting_point < 2:
                day(the_current_day, daily_limit)
            variables.daily_limit = daily_limit
            history.database(twitter_user_name, the_current_day)
            if variables.sql_daily_limit < daily_limit:
                if variables.unisoftdev_new_tweet > 0:
                    variables.unisoftdev_new_tweet = 0
                    print('tweet sent')
                    add_contact(user_name)
                    api.update_status('@'+str(user_name)+' '+greetings+third_answer, tweetID)
                    random_break_time()
            else:
                restart()
                    ################################################### <---------- add new blocks of regular expressions as you see above


def start():
    global count
    global starting_point
    for i in config_data["keyword_queries"]:
        global keywords_balance
        keywords_balance =+ 1
        if starting_point > 0:
            sleep(60)
            starting_point =+ 1
        plusone = count + 1       
        while plusone < keywords_size and daily_limit > len(contacted_users):
            count =+ 1
            try:
                search_results = api.search( q=i, result_type='recent', count=90, since=str(date.today()))
                print('loading \'{}\''.format(i))
                for tweet in search_results:
                    if not tweet.retweeted:
                        sleep(2)
                        tweetID = '"' + str(tweet.id) + '"'
                        user_name = '"' + str(tweet.user.screen_name) + '"'
                        text = '"' + tweet.text + '"' 
                        exchangable_characteds = ["<", ">", "=", "$", "__", "%", "*", "&", "~", "select", "remove", "del", "exec", "append", "create", "insert"]                   
                        for bad_variable in exchangable_characteds:
                            user_name = user_name.replace(bad_variable, "replaced_term_or_characted")
                        for bad_variable in exchangable_characteds:
                            text = text.replace(bad_variable, "replaced")
                    tweet_dict = {"tweetID": tweetID, "user_name": user_name, "text": text}                   
                    global ndata
                    ndata = tweet_dict
                    for negative_keywords in config_data["negative_keywords"]:
                        if negative_keywords not in text: 
                            twitterbot_loads_tweets()
            except:
                print('check out config file and login info')
                print('sleep for 1-2 minutes')
                random_break_time()
        else:
            restart() 

if keywords_size < keywords_balance:
    restart()

    
    


