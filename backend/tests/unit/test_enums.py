from app.db import UserRole 

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
    assert UserRole.USER.name==UserRole.USER.value=="USER"
    assert UserRole.ADMIN.name==UserRole.ADMIN.value=="ADMIN"
    assert UserRole.VIEWER.name==UserRole.VIEWER.value=="VIEWER"