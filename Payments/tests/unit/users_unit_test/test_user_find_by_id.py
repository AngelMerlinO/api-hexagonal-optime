import pytest
from unittest.mock import Mock
from src.users.application.UserFindById import UserFindById

def test_find_user_by_id_success():
    user_repository_mock = Mock()
    user_mock = Mock()

    user_repository_mock.find_by_id.return_value = user_mock

    user_finder = UserFindById(user_repository_mock)
    result = user_finder.find_by_identifier("1")

    assert result == user_mock

def test_find_user_by_id_not_found():
    user_repository_mock = Mock()
    user_repository_mock.find_by_id.return_value = None

    user_finder = UserFindById(user_repository_mock)

    with pytest.raises(ValueError):
        user_finder.find_by_identifier("1")