import logging
import os
import requests

from volara_proof.models.tweet_info import TweetInfo
from volara_proof.constants import VOLARA_API_URL


class RewardsStorage:
    def post_rewards(
        self,
        file_id: str,
        miner_address: str,
        file_score: float,
        tweet_scores: list[TweetInfo],
    ) -> None:
        tweet_records = [
            {
                "tweetId": tweet_score.tweet_id,
                "userId": tweet_score.user_id,
                "ownershipScore": tweet_score.score,
            }
            for tweet_score in tweet_scores
        ]
        request_body = {
            "fileId": file_id,
            "minerAddress": miner_address,
            "tweetCount": len(tweet_scores),
            "submissionScore": file_score,
            "tweetRecords": tweet_records,
        }
        try:
            resp = requests.post(
                url=f"{VOLARA_API_URL}/v1/validator/submit-validation",
                json=request_body,
                headers={"Authorization": f"Bearer {os.environ['VOLARA_API_KEY']}"},
            )
            resp.raise_for_status()
            logging.info("Succesfully uploaded rewards to validator.")
            return resp.json()
        except Exception:
            logging.exception(
                "[CRITICAL FAILURE] Failed to upload rewards to the director."
            )
            raise
