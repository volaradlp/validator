import logging
import os
import requests

from volara_proof.models.user_data import UserData
from volara_proof.constants import VOLARA_API_URL


class UserInfoStorage:
    def verify_user(self, user_info: UserData) -> bool:
        request_body = {
            "handle": user_info.handle,
            "walletAddress": user_info.wallet_address,
        }
        try:
            resp = requests.post(
                url=f"{VOLARA_API_URL}/v1/validator/validate-user",
                json=request_body,
                headers={"Authorization": f"Bearer {os.environ['VOLARA_API_KEY']}"},
            )
            resp.raise_for_status()
            logging.info("Succesfully determined if user exists.")
            return resp.json()["userValidated"]
        except Exception:
            logging.exception("[CRITICAL FAILURE] Failed to determine if user exists.")
            raise

    def process_profile(self, user_info: UserData) -> None:
        request_body = {
            "walletAddress": user_info.wallet_address,
        }
        try:
            resp = requests.post(
                url=f"{VOLARA_API_URL}/v1/validator/profile-processed",
                json=request_body,
                headers={"Authorization": f"Bearer {os.environ['VOLARA_API_KEY']}"},
            )
            resp.raise_for_status()
            logging.info("Succesfully processed profile.")
            return resp.json()["userValidated"]
        except Exception:
            logging.exception("[CRITICAL FAILURE] Failed to process profile.")
            raise
