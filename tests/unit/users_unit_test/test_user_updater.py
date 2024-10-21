import pytest
from unittest.mock import Mock
from src.users.application.UserUpdater import UserUpdater

def test_update_user_success():
    user_repository_mock = Mock()

    user_mock = Mock()
    user_repository_mock.find_by_id.return_value = user_mock

    user_updater = UserUpdater(user_repository_mock)

    identifier = "1"
    new_username = "updateduser"
    new_email = "updated@example.com"
    new_password = "newpassword123"

    user_updater.update(identifier, new_username, new_email, new_password)

    user_repository_mock.update.assert_called_once()

def test_update_user_not_found():
    user_repository_mock = Mock()
    user_repository_mock.find_by_id.return_value = None

    user_updater = UserUpdater(user_repository_mock)

    identifier = "1"
    with pytest.raises(ValueError):
        user_updater.update(identifier, "newuser", "new@example.com", "newpassword")