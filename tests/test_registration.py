import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Testlerden önce veri tabanını oluşturmak ve testlerden sonra temizlemek için kullanılan test düzeneği."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Test sırasında veri tabanı bağlantısı oluşturur ve testten sonra bağlantıyı kapatır."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Veri tabanı ve 'users' tablosunun oluşturulmasını test eder."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "'users' tablosu veri tabanında bulunmalıdır."

def test_add_new_user(setup_database, connection):
    """Yeni bir kullanıcının eklenmesini test eder."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Kullanıcı veri tabanına eklenmiş olmalıdır."

# İşte yazabileceğiniz bazı testler:
"""
Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme.
Başarılı kullanıcı doğrulamasını test etme.
Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.
Yanlış şifreyle doğrulama yapmayı test etme.
Kullanıcı listesinin doğru şekilde görüntülenmesini test etme.
"""
# Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme.

def test_add_existing_user(setup_database):
    """Var olan bir kullanıcı adıyla tekrar kullanıcı eklemeye çalışmayı test eder."""
    add_user('duplicate_user', 'dup1@example.com', 'pass123')
    result = add_user('duplicate_user', 'dup2@example.com', 'pass456')
    assert result is False, "Aynı kullanıcı adıyla ikinci bir kayıt oluşturulamamalıdır."


    # Başarılı kullanıcı doğrulamasını test etme
def test_authenticate_user_success(setup_database):
    """Başarılı kullanıcı doğrulamasını test eder."""
    add_user('auth_success', 'success@example.com', 'correct_password')
    assert authenticate_user('auth_success', 'correct_password') is True


    # Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.
def test_authenticate_non_existent_user(setup_database):
    """Var olmayan bir kullanıcıyla doğrulama yapmayı test eder."""
    assert authenticate_user('ghost_user', 'some_password') is False


    # Yanlış şifreyle doğrulama yapmayı test etme.
def test_authenticate_wrong_password(setup_database):
    """Yanlış şifreyle doğrulama yapmayı test eder."""
    add_user('wrong_pass_user', 'wrong@example.com', 'real_password')
    assert authenticate_user('wrong_pass_user', 'wrong_password') is False


    # Kullanıcı listesinin doğru şekilde görüntülenmesini test etme.
def test_display_users(setup_database, capsys):
    """Kullanıcı listesinin doğru şekilde görüntülenmesini (print edilmesini) test eder."""
    add_user('display_user', 'display@example.com', 'pass123')
    display_users()
    captured = capsys.readouterr()
    assert "Kullanıcı adı: display_user" in captured.out
    assert "E-posta: display@example.com" in captured.out

