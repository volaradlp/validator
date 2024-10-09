import typing as T
import numpy as np
import logging
import json
from random import sample

import volara_proof.exceptions
from volara_proof.buffers.tweets import Tweets
from volara_proof.buffers.tweet import Tweet
from volara_proof.models.tweet_info import TweetInfo
from volara_proof.storage.tweet_info import TweetInfoStorage
from volara_proof.models.proof_config import ProofConfig
from volara_proof.scraper.VolaraScraper import VolaraScraper


def get_scraper(config: ProofConfig):
    cookies = json.loads(config.cookies)
    return VolaraScraper(cookies=cookies)


tweet_info_storage = TweetInfoStorage()

NIL_RESPONSE_INVALID = {
    "is_valid": False,
    "file_score": 0,
    "tweet_info": list(),
    "unique_tweets": 0,
    "total_tweets": 0,
}

NIL_RESPONSE_VALID = {
    "is_valid": True,
    "file_score": 0,
    "tweet_info": list(),
    "unique_tweets": 0,
    "total_tweets": 0,
}


def proof_of_quality(tweets_data: Tweets, file_id: str, config: ProofConfig):
    if not _no_duplicates(tweets_data):
        return NIL_RESPONSE_INVALID
    unique_tweets = _unique_tweets(tweets_data, file_id)
    if len(unique_tweets) == 0:
        return NIL_RESPONSE_VALID
    tweets_validated = _validate_tweets(tweets_data, unique_tweets, config)
    if not tweets_validated:
        return NIL_RESPONSE_INVALID
    tweet_info = _score_tweets(tweets_data, unique_tweets)
    file_score = min(sum([tweet.score for tweet in tweet_info]) / 100_000, 1)
    return {
        "is_valid": True,
        "file_score": file_score,
        "tweet_info": tweet_info,
        "unique_tweets": len(unique_tweets),
        "total_tweets": tweets_data.TweetsLength(),
    }


def _validate_tweets(
    tweets_data: Tweets, unique_tweets: T.Set[str], config: ProofConfig
):
    unique_tweet_data = [
        tweets_data.Tweets(i)
        for i in range(tweets_data.TweetsLength())
        if tweets_data.Tweets(i).TweetId().decode() in unique_tweets
    ]

    # Sampling 10 tweets gives us ~65% confidence at 10% malicious rate
    sample_count = _calc_confidence(0.65, 0.1, len(unique_tweet_data))
    tweet_sample = sample(range(len(unique_tweet_data)), sample_count)

    tweet_ids = [unique_tweet_data[i].TweetId().decode() for i in tweet_sample]
    scraped_tweets = _scrape_tweets(tweet_ids, config)

    for tweet_data_i, tweet in zip(tweet_sample, scraped_tweets):
        if "result" not in tweet:  # Does this allow fake tweet attacks?
            continue
        typename = tweet["result"]["__typename"]
        if typename == "TweetUnavailable":
            continue
        if "tweet" in tweet["result"]:
            text = tweet["result"]["tweet"]["legacy"]["full_text"]
        else:
            text = tweet["result"]["legacy"]["full_text"]
        if text != unique_tweet_data[tweet_data_i].Text().decode():
            return False
    return True


def _scrape_tweets(tweet_ids: list[str], config: ProofConfig) -> list[dict[str, T.Any]]:
    try:
        scraper = get_scraper(config)
        tweets = scraper.get_tweets_by_ids(tweet_ids)
        return tweets
    except Exception as e:
        logging.exception(
            f"[EPHEMERAL ERROR]: Failed to scrape {len(tweet_ids)} tweets."
        )
        raise volara_proof.exceptions.VolaraApiServerException(e)


def _no_duplicates(tweets_data: Tweets) -> bool:
    tweet_ids: set[bytes] = set()
    for i in range(tweets_data.TweetsLength()):
        if tweets_data.Tweets(i).TweetId() in tweet_ids:
            return False
        tweet_ids.add(tweets_data.Tweets(i).TweetId())
    return True


def _unique_tweets(tweets_data: Tweets, file_id: str) -> T.Set[str]:
    tweet_ids = [
        str(tweets_data.Tweets(i).TweetId().decode())
        for i in range(tweets_data.TweetsLength())
    ]
    tweet_id_existance = tweet_info_storage.get(tweet_ids, file_id)
    unique_tweets = set(
        [
            tweet_id
            for tweet_id, exists in zip(tweet_ids, tweet_id_existance)
            if not exists
        ]
    )
    return unique_tweets


def _form_tweet_info(tweet: T.Optional[Tweet], score: float) -> TweetInfo:
    if tweet is None:
        raise Exception("Invalid none tweet")
    return TweetInfo(
        tweet_id=tweet.TweetId().decode(),
        user_id=tweet.UserId().decode(),
        score=score,
    )


def _score_tweets(tweets_data: Tweets, unique_tweets: T.Set[str]) -> list[TweetInfo]:
    # TODO: Evaluate dynamic score
    scored_tweets: list[TweetInfo] = []
    for i in range(tweets_data.TweetsLength()):
        if tweets_data.Tweets(i).TweetId().decode() not in unique_tweets:
            continue
        scored_tweets.append(_form_tweet_info(tweets_data.Tweets(i), 10))
    return scored_tweets


def _calc_confidence(
    desired_confidence: float, malicious_rate: float, sample_size: int
):
    if sample_size < 100:
        return 1
    return int(np.ceil(np.log(1 - desired_confidence) / np.log(1 - malicious_rate)))
