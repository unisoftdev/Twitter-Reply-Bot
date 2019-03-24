# For a GUI, better performance, more functions, and easiness to use... Check out: www.unisoftdev.tech

'''
* @ The Free Version Of a Web Crawler
* Created By: Juraj Vysvader
* Author's profile: https://www.linkedin.com/in/jurajvysvader
                    https://www.linkedin.com/company/unisoftdev 
* Creation date: 10.3.2019
* Business website: https://www.unisoftdev.tech
* @license http://www.gnu.org/copyleft/lgpl.html GNU/GPL
* @Copyright (C) 2019 Juraj Vysvader. All rights reserved.
'''

import sqlite3 as lite
import variables


def write_new_user(con, twitter_user_name, the_current_day):
    cursor = con.cursor()
    cursor.execute("INSERT INTO user (date, user) VALUES (?, ?)",
                (the_current_day, twitter_user_name))
    inserted_id = cursor.lastrowid
    con.commit()
    return inserted_id


def database(twitter_user_name, the_current_day):
    twitter_user_name = twitter_user_name
    the_current_day = the_current_day
    is_it_found = 0
    twitter_user_name = twitter_user_name.lower()
    exchangable_characteds = ["<", ">", "=", "$", "__", "%", "*", "&", "~", "select", "remove", "del", "exec", "append", "create", "insert"]
    for bad_variable in exchangable_characteds:
        twitter_user_name = twitter_user_name.replace(bad_variable, "replaced_term_or_characted")
    con = lite.connect('twitter_customer_reply_bot.sqlite3')
    cur = con.cursor()
    with con:
        try:
            cur.execute("SELECT * FROM user WHERE user = ?", (twitter_user_name,)) 
            con.commit()
            row = cur.fetchone()
            if row is None:
                write_new_user(con, twitter_user_name, the_current_day)
                is_it_found = 0
            else:
                is_it_found =+ 1 
                variables.unisoftdev_new_tweet = 0           
        except:
            try:
                is_it_found =+ 1
                write_new_user(con, twitter_user_name, the_current_day)
                variables.sql_daily_limit =+ 1
                variables.unisoftdev_new_tweet = 1
            except:
                print("error")
        if is_it_found < 1:
                variables.sql_daily_limit =+ 1 
                variables.unisoftdev_new_tweet = 1
                print('new tweet on the way')
        else:
            variables.unisoftdev_new_tweet = 0

