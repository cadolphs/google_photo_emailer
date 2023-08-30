import pytest

from photo_emailer.logic.credentials import Credentials
from photo_emailer.infrastructure.credentials_refresher import (
    CredentialsRefresher,
    RefreshError,
)


def test_credentials_refresher_can_refresh_credentials_if_expired():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    refresher = CredentialsRefresher.create_null()

    refreshed_creds = refresher.refresh(creds)

    assert not refreshed_creds.is_expired()


def test_testinstance_raises_error():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    refresher = CredentialsRefresher.create_test_instance_that_errors()

    with pytest.raises(RefreshError):
        refreshed_creds = refresher.refresh(creds)
