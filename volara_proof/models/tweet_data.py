"""
Contains the dataclass models for the Tweet data structure
"""

import datetime as dt
import typing as T
from dataclasses import dataclass


@dataclass
class TweetData:
    handle: str
    tweet_id: str
    text: str
    likes: int
    retweets: int
    replies: int
    quotes: int
    created_at: dt.datetime
    subtweet_id: T.Optional[str] = None
