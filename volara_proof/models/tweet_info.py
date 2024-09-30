from dataclasses import dataclass


@dataclass(frozen=True, slots=True, order=True)
class TweetInfo:
    tweet_id: str
    user_id: str
    score: float
