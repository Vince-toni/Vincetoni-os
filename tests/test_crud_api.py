from database.crud import get_or_create_user


def test_get_or_create_user_is_exposed():
    assert callable(get_or_create_user)
