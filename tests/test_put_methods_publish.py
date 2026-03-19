import pytest
import requests


class TestPublishMethods:

    # Тесты скачивания по публичной ссылке (test_publish_file, test_publish_and_access_public_resource) завершаются с
    # ошибкой из-за капчи.
    # Яндекс блокирует автоматические запросы к публичным ссылкам
    # (https://yadi.sk/...) и возвращает страницу с капчей.

    def test_publish_file(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка файла
        file_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Публикация файла
        publish_response = api_client.publish_resource(path=file_path)
        assert publish_response.status_code in [200, 201, 202]

        # Проверка получения публичной ссылки
        public_url = api_client.get_public_url(path=file_path)
        assert public_url is not None
        assert public_url.startswith("http")

        # Проверка доступности публичной ссылки
        download_response = requests.get(public_url)
        assert download_response.status_code == 200
        assert test_file_content in download_response.text

    def test_publish_folder(self, api_client, test_base_folder, random_folder_name):
        # Создание папки
        folder_path = f"{test_base_folder}/{random_folder_name}"
        api_client.create_folder(path=folder_path)

        # Публикация папки
        publish_response = api_client.publish_resource(path=folder_path)
        assert publish_response.status_code in [200, 201, 202]

        # Проверка получения публичной ссылки
        public_url = api_client.get_public_url(path=folder_path)
        assert public_url is not None
        assert public_url.startswith("http")

    def test_unpublish_file(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка и публикация файла
        file_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        api_client.publish_resource(path=file_path)
        public_url_before = api_client.get_public_url(path=file_path)
        assert public_url_before is not None

        # Отмена публикации
        unpublish_response = api_client.unpublish_resource(path=file_path)
        assert unpublish_response.status_code in [200, 201, 202]

    def test_publish_nonexistent_resource(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/nonexistent_{random_filename}"
        response = api_client.publish_resource(path=path)
        assert response.status_code in [404, 400, 409]

    def test_publish_and_access_public_resource(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка файла
        file_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Публикация
        api_client.publish_resource(path=file_path)

        # Получение публичной ссылки
        public_url = api_client.get_public_url(path=file_path)
        assert public_url is not None

        # Доступ к файлу по публичной ссылке
        response = requests.get(public_url)
        assert response.status_code == 200
        assert test_file_content in response.text

        # Отмена публикации
        api_client.unpublish_resource(path=file_path)
