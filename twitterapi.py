import tweepy
import os

class TwitterController():
    def __init__(self, twitter_user=None):
        auth = tweepy.OAuthHandler(
            os.getenv("TWITTER_AUTH_KEY"),
            os.getenv("TWITTER_AUTH_SECRET")
            )
        auth.set_access_token(
            os.getenv("TWITTER_ACCESS_KEY"),
            os.getenv("TWITTER_ACCESS_SECRET")
            )
        self.auth = auth
        self.twitter_controller = tweepy.API(
            self.auth, wait_on_rate_limit=True
            )
        self.twitter_user = twitter_user

    def get_timeline_tweets(self):
        # Returns tweets of user's timeline in a list
        tweets = []
        for tweet in tweepy.Cursor(
                     self.twitter_controller.user_timeline,
                     id=self.twitter_user
                     ).items():
            tweets.append(tweet)
        return tweets

    def get_following_list(self):
        following_list = []
        for friend in tweepy.Cursor(
                      self.twitter_controller.get_friends,
                      id=self.twitter_user
                      ).items(20):
            following_list.append(friend)
        return following_list

    def get_selected_following(self, user):
        following_list = []
        for friend in tweepy.Cursor(
                      self.twitter_controller.get_friends, id=user
                      ).items():
            following_list.append(friend)
        return following_list

    def get_followers(self):
        follower_list = []
        for follower in tweepy.Cursor(
                        self.twitter_controller.followers,
                        id=self.twitter_user
                        ).items():
            follower_list.append(follower)
        return follower_list

    def get_selected_followers(self, user):
        follower_list = []
        for follower in tweepy.Cursor(
                        self.twitter_controller.followers,
                        id=user
                        ).items():
            follower_list.append(follower)
        return follower_list

    def get_user_info(self, user):
        return self.twitter_controller.get_user(user)
