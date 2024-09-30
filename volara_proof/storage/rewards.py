import logging
import os
import json
from uuid import uuid1

from aiohttp import ClientSession, ClientTimeout

from volara_proof.models.tweet_info import TweetInfo
from volara_proof.constants import VOLARA_API_URL


class RewardsStorage:
    async def post_rewards(
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
            async with ClientSession(timeout=ClientTimeout(30)) as session:
                async with session.post(
                    url=f"{VOLARA_API_URL}/v1/validator/submit-validation",
                    json=request_body,
                    headers={"Authorization": f"Bearer {os.environ['VOLARA_API_KEY']}"},
                ) as resp:
                    resp.raise_for_status()
                    resp = await resp.json()
                    logging.info("Succesfully uploaded rewards to validator.")
        except Exception:
            logging.exception(
                "[CRITICAL FAILURE] Failed to upload rewards to the director."
            )
            try:
                os.mkdir(".critical_reward_failures/")
            except FileExistsError:
                pass
            with open(f".critical_reward_failures/{str(uuid1())}", "+w") as f:
                f.write(json.dumps(request_body))
            raise
