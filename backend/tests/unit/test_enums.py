from app.db import DataAccess, UserRole


def test_user_role_ordering():
    assert UserRole.VIEWER < UserRole.ADMIN
    assert UserRole.VIEWER < UserRole.USER
    assert UserRole.USER < UserRole.ADMIN
    assert UserRole.ADMIN > UserRole.VIEWER
    assert UserRole.ADMIN > UserRole.USER
    assert UserRole.USER > UserRole.VIEWER
    assert UserRole.ADMIN == UserRole.ADMIN
    assert UserRole.VIEWER == UserRole.VIEWER
    assert UserRole.USER == UserRole.USER
    assert UserRole.USER.name == UserRole.USER.value == "USER"
    assert UserRole.ADMIN.name == UserRole.ADMIN.value == "ADMIN"
    assert UserRole.VIEWER.name == UserRole.VIEWER.value == "VIEWER"

    assert UserRole.VIEWER <= UserRole.USER <= UserRole.ADMIN


def test_data_access_ordering():
    assert DataAccess.PUBLIC < DataAccess.INTERNAL
    assert DataAccess.PUBLIC < DataAccess.RESTRICTED
    assert DataAccess.PUBLIC < DataAccess.CONFIDENTIAL
    assert DataAccess.INTERNAL > DataAccess.PUBLIC
    assert DataAccess.RESTRICTED > DataAccess.PUBLIC
    assert DataAccess.CONFIDENTIAL > DataAccess.PUBLIC
    assert DataAccess.PUBLIC == DataAccess.PUBLIC
    assert DataAccess.PUBLIC.name == DataAccess.PUBLIC.value == "PUBLIC"

    assert DataAccess.INTERNAL < DataAccess.RESTRICTED
    assert DataAccess.INTERNAL < DataAccess.CONFIDENTIAL
    assert DataAccess.RESTRICTED > DataAccess.INTERNAL
    assert DataAccess.CONFIDENTIAL > DataAccess.INTERNAL
    assert DataAccess.INTERNAL == DataAccess.INTERNAL
    assert DataAccess.INTERNAL.name == DataAccess.INTERNAL.value == "INTERNAL"

    assert DataAccess.RESTRICTED < DataAccess.CONFIDENTIAL
    assert DataAccess.CONFIDENTIAL > DataAccess.RESTRICTED
    assert DataAccess.RESTRICTED == DataAccess.RESTRICTED
    assert DataAccess.RESTRICTED.name == DataAccess.RESTRICTED.value == "RESTRICTED"

    assert DataAccess.CONFIDENTIAL == DataAccess.CONFIDENTIAL
    assert (
        DataAccess.CONFIDENTIAL.name == DataAccess.CONFIDENTIAL.value == "CONFIDENTIAL"
    )

    assert (
        DataAccess.PUBLIC
        <= DataAccess.INTERNAL
        <= DataAccess.RESTRICTED
        <= DataAccess.CONFIDENTIAL
    )
