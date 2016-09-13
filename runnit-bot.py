"""

This script is used to helpout AutoMod on some things it can't do.

"""

import datetime
import os,sys
import praw
import logging
import re
import sched, time

USERNAME=os.environ['USER']
PASSWORD=os.environ['PASSWORD']
AUTHOR=os.environ['AUTHOR']
CommentsRemoved = set();
def login():
  r = praw.Reddit('RunnitAutoMod test by ' + AUTHOR);
  r.login(USERNAME, PASSWORD, disable_warning=True)
  return r

    
def message_me(reddit_session ):
  title = 'logged in added'
  body= 'I was able to login and send you a message!'
  reddit_session.send_message(AUTHOR, title, body)

def comments_by_user(reddit_session, subreddit, user_name):
    all_comments = reddit_session.get_comments(subreddit, limit="none")
    user = praw.objects.Redditor(reddit_session,user_name=user_name) 
    user_comments = [comment for comment in all_comments if comment.author == user]
    return user_comments;

def run(reddit_session):
   #find all comments by AutoModerator
   comments = comments_by_user(reddit_session, 'Running', 'AutoModerator')
   logging.info(str(datetime.datetime.now()) + ':Found ' + str(len(comments)) + ' for AutoModerator');

   #get all comments with negative score
   negative_score_comments = [ c for c in comments if c.score < 0 ]
   logging.info(str(datetime.datetime.now()) + ':Found ' + str(len(negative_score_comments)) + ' negative for AutoModerator');
   

   #remove the comments
   for comment in negative_score_comments:
     logging.debug(comment);
     if comment not in CommentsRemoved:
       comment.remove();
       CommentsRemoved.add(comment);

   # message the author
   if len(negative_score_comments) > 0:
       title = 'Removed AutoMod comments due to negative score';
       body = 'Removed the following comments. \n';
       body += '\n'.join([comment.permalink for comment in negative_score_comments]);
       reddit_session.send_message(AUTHOR, title, body)

if __name__ == '__main__':

   #login 
   r = login();

   #Search every 5 minutes.
   while True:
       logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
       logging.info(str(datetime.datetime.now()) + ":Starting")
       
       #run the bot! check for negative automod comments in /r/running
       run(r);

       logging.info(str(datetime.datetime.now()) + ":Ending") 

       #done for now, check again in 5 minutes.
       time.sleep(300);
