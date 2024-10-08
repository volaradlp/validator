import math
import requests

from twitter.scraper import Scraper, Operation, batch_ids
from twitter.util import get_headers, build_params, find_key, get_cursor


class VolaraScraper(Scraper):
    def get_tweets_by_ids(self, tweet_ids: list[str]):
        operation = Operation.TweetResultsByRestIds
        queries = list(batch_ids(tweet_ids))
        keys, _, _ = operation
        _queries = [{k: q} for q in queries for k, v in keys.items()]
        resp = self._process_sync(operation, _queries)
        scraped_tweets = resp[0][0].json()
        return scraped_tweets["data"]["tweetResult"]

    def _process_sync(self, operation: tuple, queries: list[dict], **kwargs):
        headers = self.session.headers if self.guest else get_headers(self.session)
        cookies = self.session.cookies
        return [
            self._paginate_sync(dict(headers), dict(cookies), operation, **q, **kwargs)
            for q in queries
        ]

    def _paginate_sync(
        self,
        headers: dict[str, str],
        cookies: dict[str, str],
        operation: tuple,
        **kwargs,
    ):
        limit = kwargs.pop("limit", math.inf)
        cursor = kwargs.pop("cursor", None)
        is_resuming = False
        dups = 0
        DUP_LIMIT = 3
        if cursor:
            is_resuming = True
            res = []
            ids = set()
        else:
            try:
                r = self._query_sync(operation, headers, cookies, **kwargs)
                initial_data = r.json()
                res = [r]
                ids = {x for x in find_key(initial_data, "rest_id") if x[0].isnumeric()}

                cursor = get_cursor(initial_data)
            except Exception as e:
                if self.debug:
                    self.logger.error(f"Failed to get initial pagination data: {e}")
                return
        while (dups < DUP_LIMIT) and cursor:
            prev_len = len(ids)
            if prev_len >= limit:
                break
            try:
                r = self._query_sync(
                    operation, headers, cookies, cursor=cursor, **kwargs
                )
                data = r.json()
            except Exception as e:
                if self.debug:
                    self.logger.error(f"Failed to get pagination data\n{e}")
                return
            cursor = get_cursor(data)
            ids |= {x for x in find_key(data, "rest_id") if x[0].isnumeric()}

            if self.debug:
                self.logger.debug(f"Unique results: {len(ids)}\tcursor: {cursor}")
            if prev_len == len(ids):
                dups += 1
            res.append(r)
        if is_resuming:
            return res, cursor
        return res

    def _query_sync(
        self,
        operation: tuple,
        headers: dict[str, str],
        cookies: dict[str, str],
        **kwargs,
    ) -> requests.Response:
        keys, qid, name = operation
        params = {
            "variables": Operation.default_variables | kwargs,
            "features": Operation.default_features,
        }
        params = build_params(params)
        resp = requests.get(
            f"https://twitter.com/i/api/graphql/{qid}/{name}",
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=20,
        )
        try:
            self.rate_limits[name] = {
                k: int(v) for k, v in resp.headers.items() if "rate-limit" in k
            }
        except Exception as e:
            self.logger.debug(f"{e}")
        return resp
