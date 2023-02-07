import tweepy
import datetime
from datetime import datetime, timezone

# set up authorization (consumer_token, consumer_secret)
auth = tweepy.OAuthHandler('consumer_token', 'consumer_secret')

# set up access (access_token and access_token_secret)
auth.set_access_token('access_token', 'access_token_secret')

# calling the api
api = tweepy.API(auth, wait_on_rate_limit=True)


# unfollows all twitter users that do not follow you back and have less than (int)min_num_followers
# ex) unfollow_twitter_user(1000) will unfollow everyone who doesn't follow you back and has less than 1000 followers
def unfollow_twitter_user(min_num_followers):
    followers = api.get_follower_ids(screen_name=api.verify_credentials().screen_name)
    following = api.get_friend_ids(screen_name=api.verify_credentials().screen_name)
    unfollow_count = 0

    # go through each user you are following
    for user in following:
        # if user is not following you back
        if user not in followers:
            try:
                user_info = api.get_user(user_id=str(user))  # get user info
                num_followers = user_info.followers_count  # get their number of followers
                handle = user_info.name  # get their username
                print(f'checking: {handle} with {num_followers} followers')

                if num_followers < min_num_followers:
                    print(f'unfollowing: {handle} with {num_followers} followers')
                    api.destroy_friendship(user_id=user)
                    unfollow_count+=1
                else:
                    print(f'user has more than {min_num_followers} followers')
            except tweepy.errors.TweepyException as e:
                print(e)
        else:
            pass


# used to check if a user is inactive based on the (int)max_num_days since they last tweeted
# ex) is_inactive_user(user, 60) will return True if they have not tweeted anything within the lst 60 days
def is_inactive_user(user, max_num_days):
    user_info = api.get_user(user_id=str(user))  # get user info
    handle = user_info.name  # get username
    print(f'checking: {handle}')

    tweets_list = api.user_timeline(user_id=str(user), count=1)  # get the last tweet in list format

    # make sure the account actually has tweets to check
    if len(tweets_list) >=1:
        tweet = tweets_list[0]  # get the first tweet object
        print(f'last tweet created at: {tweet.created_at}')

        days_since_last_tweet = (datetime.now(timezone.utc) - tweet.created_at).days # get # of days since their last tweet
        print(f'Days since last tweet: {days_since_last_tweet}')

        if days_since_last_tweet > max_num_days:
            print(f'Handle: {handle} is inactive')
            return True
    else:
        print(f'Handle: {handle} has no tweets or is private. Ignoring...')
    return False


# unfollows all twitter users that have not tweet since (int)max_num_days
# (bool)req_follow_back: set to True if you only want to unfollow those who dont follow you back
def unfollow_inactive_twitter_user(max_num_days, req_follow_back):
    following = api.get_friend_ids(screen_name=api.verify_credentials().screen_name)
    unfollow_count = 0

    # if we don't want to unfollow anyone that is following us
    if req_follow_back:
        followers = api.get_follower_ids(screen_name=api.verify_credentials().screen_name)
        # go through every user you're following
        for user in following:
            # if user is not following you back
            if user not in followers:
                try:
                    # if user has not tweeted in max_num_days
                    if is_inactive_user(user, max_num_days):
                        print('unfollowing...')
                        api.destroy_friendship(user_id=user)
                        unfollow_count+=1
                    else:
                        print(f'Tweet happened less than {max_num_days} days ago...not unfollowing and checking the next user')
                except tweepy.errors.TweepyException as e:
                    print(e)
            else:
                pass
    # if req_follow_back is False we don't care if they are following us back
    else:
        for user in following:
            try:
                if is_inactive_user(user, max_num_days):
                    print('unfollowing...')
                    api.destroy_friendship(user_id=user)
                    unfollow_count+=1
                else:
                    print(
                        f'Tweet happened less than {max_num_days} days ago...not unfollowing and checking the next user')
            except tweepy.errors.TweepyException as e:
                print(e)

    print(f'You unfollowed a total of {unfollow_count} users')

if __name__ == "__main__":
    # unfollow anyone that hasn't tweeted in 60 days even if they follow me back
    #unfollow_inactive_twitter_user(60, False)

    # unfollow anyone that doesn't follow me back and has less than 1000 followers
    #unfollow_twitter_user(1000)
