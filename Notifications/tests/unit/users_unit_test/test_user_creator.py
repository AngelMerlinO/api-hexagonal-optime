import pytest
from unittest.mock import Mock
from src.users.application.UserCreator import UserCreator
from src.contact.domain.exceptions import ContactNotFoundException


def test_create_user_success():
    user_repository_mock = Mock()
    contact_repository_mock = Mock()

    contact_repository_mock.get_by_id.return_value = Mock()

    user_creator = UserCreator(user_repository_mock, contact_repository_mock)

    contact_id = 1
    username = "testuser"
    email = "test@example.com"
    password = "password123"

    user_creator.create(contact_id, username, email, password)

    user_repository_mock.save.assert_called_once()
    saved_user = user_repository_mock.save.call_args[0][0]

    assert saved_user.username == username
    assert saved_user.email == email
    assert saved_user.password == password

def test_create_user_contact_not_found():
    user_repository_mock = Mock()
    contact_repository_mock = Mock()

    contact_repository_mock.get_by_id.return_value = None

    user_creator = UserCreator(user_repository_mock, contact_repository_mock)

    contact_id = 1
    username = "testuser"
    email = "test@example.com"
    password = "password123"

    with pytest.raises(ContactNotFoundException):
        user_creator.create(contact_id, username, email, password)