# twitter_unfollower_bot
A python twitter bot that unfollows twitter accounts for you based on number of followers, if they follow you back, or if they are inactive (haven't tweeted for a specified number of days).

Enter in your specific consumer and access tokens in the lines for the twitter api:
auth = tweepy.OAuthHandler('consumer_token', 'consumer_secret')
auth.set_access_token('access_token','access_token_secret')

and uncomment one of these methods under if __name__ == "__main__":
# unfollow anyone that hasn't tweeted in 60 days even if they follow me back
# unfollow_inactive_twitter_user(60, False)

# unfollow anyone that doesn't follow me back and has less than 1000 followers
# unfollow_twitter_user(1000)

And it should be good to run
