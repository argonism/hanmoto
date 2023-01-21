import os

from pytwitter import Api
from dotenv import load_dotenv

from tofu_client import TofuClient


load_dotenv()
# from typing import Dict


def get_tweets() -> None:
    # token = os.environ["TWITTER_API_BEARER_TOKEN"]
    # api = Api(bearer_token=token)
    tofu_client = TofuClient()
    api = Api(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    user = api.get_users(usernames="usulity").data[0]
    print(user.id)
    tw_list = api.get_list_tweets(1612845796072001536).data
    for tweet in tw_list:
        tweet_text = tweet.text
        tofu_client.print_text(tweet_text)
    # tw_list = api.get_user_owned_lists(
    #     user_id=user.id,
    #     list_fields="follower_count",
    #     expansions="owner_id",
    #     user_fields="created_at",
    # )


if __name__ == "__main__":
    get_tweets()
