from aiohttp import ClientSession, ClientTimeout
import os

import volara_proof.exceptions
from volara_proof.constants import VOLARA_API_URL
from volara_proof.models.tweet_info import TweetInfo


class TweetInfoStorage:
    async def get_info(self, tweet_info: list[TweetInfo], file_id: str) -> list[bool]:
        return await self.get([tweet.tweet_id for tweet in tweet_info], file_id)

    async def get(self, tweet_ids: list[str], file_id: str) -> list[bool]:
        """
        Returns a list of booleans indicating whether each tweet ID exists in the index.
        """
        if len(tweet_ids) == 0:
            return []
        try:
            async with ClientSession(timeout=ClientTimeout(10)) as session:
                async with session.post(
                    f"{VOLARA_API_URL}/v1/validator/unique",
                    json={"tweetIds": tweet_ids, "fileId": file_id},
                    headers={"Authorization": f"Bearer {os.environ['VOLARA_API_KEY']}"},
                ) as resp:
                    resp.raise_for_status()
                    return [False for unique in await resp.json()]
        except Exception as e:
            raise volara_proof.exceptions.VolaraApiServerException(e)
