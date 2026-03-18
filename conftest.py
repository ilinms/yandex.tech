import pytest
import os
import tempfile
import shutil
from faker import Faker
from src.api_client import YandexDiskClient
from config import DISK_OAUTH_TOKEN, TEST_FOLDER

fake = Faker()


@pytest.fixture(scope="session")
def api_client():
    if not DISK_OAUTH_TOKEN:
        pytest.skip("Токен не найден в .env")
    return YandexDiskClient(oauth_token=DISK_OAUTH_TOKEN)


@pytest.fixture(scope="session")
def test_base_folder():
    return TEST_FOLDER


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(api_client, test_base_folder):
    """Создание базовой папки перед тестами и послеждующее удаление"""
    try:
        api_client.create_folder(path=test_base_folder)
    except Exception:
        pass

    yield

    try:
        api_client.delete_resource(path=test_base_folder, permanently=True)
    except Exception:
        pass


@pytest.fixture
def random_filename():
    return f"test_file_{fake.uuid4()}.txt"


@pytest.fixture
def random_folder_name():
    return f"test_folder_{fake.uuid4()}"


@pytest.fixture
def test_file_content():
    return f"Test content: {fake.sentence()}"


@pytest.fixture
def temp_file(test_file_content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_file_content)
        temp_path = f.name

    yield temp_path

    if os.path.exists(temp_path):
        os.remove(temp_path)