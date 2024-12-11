"""
Contains the dataclass models for the Tweet data structure
"""

from dataclasses import dataclass


@dataclass
class UserData:
    handle: str
    wallet_address: str