import pytest
from unittest.mock import Mock
from src.users.application.UserEliminator import UserEliminator

def test_delete_user_success():
    user_repository_mock = Mock()
    user_mock = Mock()

    user_repository_mock.find_by_id.return_value = user_mock

    user_eliminator = UserEliminator(user_repository_mock)
    user_eliminator.delete("1")

    user_repository_mock.delete.assert_called_once()

def test_delete_user_not_found():
    user_repository_mock = Mock()
    user_repository_mock.find_by_id.return_value = None

    user_eliminator = UserEliminator(user_repository_mock)

    with pytest.raises(ValueError):
        user_eliminator.delete("1")