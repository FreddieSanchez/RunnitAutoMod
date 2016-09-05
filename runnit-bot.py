"""

This script is used to helpout AutoMod on some things it can't do.

"""
import datetime
import os
import praw
import logging
import re
import sched, time
from authentication import USERNAME, PASSWORD, AUTHOR

def login():
  r = praw.Reddit('RunnitAutoMod test by ' + AUTHOR);
  r.login(USERNAME, PASSWORD, disable_warning=True)
  return r

    
def message_me(reddit_session ):
  title = 'logged in added'
  body= 'I was able to login and send you a message!'
  reddit_session.send_message(AUTHOR, title, body)

def comments_by_user(reddit_session, subreddit, user_name):
    all_comments = reddit_session.get_comments(subreddit)
    user = praw.objects.Redditor(reddit_session,user_name=user_name) 
    user_comments = [comment for comment in all_comments if comment.author == user]
    return user_comments;


if __name__ == '__main__':
   logging.basicConfig(filename='RunnitMod.'+ str(datetime.date.today())+'.log',level=logging.DEBUG)
   logging.info(str(datetime.datetime.now()) + ":Starting")
   #login 
   r = login()

   #find all comments by AutoModerator
   comments = comments_by_user(r, 'Running', 'AutoModerator')
   logging.info(str(datetime.datetime.now()) + ':Found ' + str(len(comments)) + ' for AutoModerator');

   #get all comments with negative score
   negative_score_comments = [ c for c in comments if c.score < 0 ]
   logging.info(str(datetime.datetime.now()) + ':Found ' + str(len(negative_score_comments)) + ' negative for AutoModerator');

   #remove the comments
   for comment in negative_score_comments:
     logging.debug(comment);
     comment.remove();

   # message the real moderators
   if len(negative_score_comments) > 0:
       title = 'Removed AutoMod comments due to negative score';
       body = 'Removed the following comments. \n';
       body += '\n'.join([comment.permalink for comment in negative_score_comments]);
       r.send_message('/r/running', title, body)

   logging.info(str(datetime.datetime.now()) + ":Ending")
 
