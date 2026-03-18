import pytest
import requests


class TestPostMethods:

    def test_upload_and_copy_file(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка файла
        src_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=src_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Копирование файлф
        dst_path = f"{test_base_folder}/copy_{random_filename}"
        response = api_client.copy_resource(from_path=src_path, to_path=dst_path)
        assert response.status_code in [201, 202, 409]

        # Проверяка копии
        resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in resources["_embedded"]["items"]]
        assert random_filename in items
        assert f"copy_{random_filename}" in items

    def test_upload_and_move_file(self, api_client, test_base_folder, random_filename, test_file_content):
        # Создание подпапку
        subfolder = f"{test_base_folder}/move_subfolder"
        api_client.create_folder(path=subfolder)

        # Загрузка файла в корень тестовой папки
        src_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=src_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Перемещение файла в подпапку
        dst_path = f"{subfolder}/{random_filename}"
        response = api_client.move_resource(from_path=src_path, to_path=dst_path)
        assert response.status_code in [201, 202]

        # Проверка отсутствия в корне
        resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in resources["_embedded"]["items"]]
        assert random_filename not in items

        # Проверка подпапке
        sub_resources = api_client.get_resources(path=subfolder)
        sub_items = [item["name"] for item in sub_resources["_embedded"]["items"]]
        assert random_filename in sub_items
