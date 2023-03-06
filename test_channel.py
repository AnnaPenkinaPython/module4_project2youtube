from main import Youtube
import pytest


def test_str():
    channel_id = Youtube("UCMCgOm8GZkHp8zJ6l7_hIuA")
    assert channel_id.__str__() == "Youtube-channel: вДудь"


def test_add():
    channel_id = Youtube("UCByhZ-JEe5OOZSuq0uaXOng")
    other_id = Youtube("UCMCgOm8GZkHp8zJ6l7_hIuA")
    assert channel_id + other_id == "98900010300000"


def test_lt():
    channel_id = Youtube("UCByhZ-JEe5OOZSuq0uaXOng")
    other_id = Youtube("UCMCgOm8GZkHp8zJ6l7_hIuA")
    assert (channel_id.subscriber_count > other_id.subscriber_count) is True
