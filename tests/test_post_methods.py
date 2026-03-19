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

    def test_copy_nonexistent_resource(self, api_client, test_base_folder, random_filename):
        # копированиe несуществующего ресурса
        src_path = f"{test_base_folder}/nonexistent_{random_filename}"
        dst_path = f"{test_base_folder}/copy_{random_filename}"
        response = api_client.copy_resource(from_path=src_path, to_path=dst_path)
        assert response.status_code in [404,400]

    def test_copy_to_invalid_path(self, api_client, test_base_folder, random_filename, test_file_content):

        src_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=src_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # копированиe в недопустимый путь
        invalid_path = f"{test_base_folder}/invalid:name"
        response = api_client.copy_resource(from_path=src_path, to_path=invalid_path)
        assert response.status_code in [400, 404]

    def test_copy_to_nonexistent_folder(self, api_client, test_base_folder, random_filename, test_file_content):
        src_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=src_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # копирование в несуществующую папку
        nonexistent_folder = f"{test_base_folder}/nonexistent_folder"
        dst_path = f"{nonexistent_folder}/{random_filename}"
        response = api_client.copy_resource(from_path=src_path, to_path=dst_path)
        assert response.status_code == 409

    def test_move_nonexistent_resource(self, api_client, test_base_folder, random_filename):
        # перемещение несуществующего ресурса
        src_path = f"{test_base_folder}/nonexistent_{random_filename}"
        dst_path = f"{test_base_folder}/move_{random_filename}"
        response = api_client.move_resource(from_path=src_path, to_path=dst_path)
        assert response.status_code in [404, 400]

    def test_move_to_invalid_path(self, api_client, test_base_folder, random_filename, test_file_content):

        src_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=src_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # перемещение в недопустимый путь
        invalid_path = f"{test_base_folder}/invalid:name"
        response = api_client.move_resource(from_path=src_path, to_path=invalid_path)
        assert response.status_code in [400, 404]

    def test_move_to_nonexistent_folder(self, api_client, test_base_folder, random_filename, test_file_content):
        src_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=src_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # перемещение в несуществующую папку
        nonexistent_folder = f"{test_base_folder}/nonexistent_folder"
        dst_path = f"{nonexistent_folder}/{random_filename}"
        response = api_client.move_resource(from_path=src_path, to_path=dst_path)
        assert response.status_code == 409

    def test_move_to_child_folder(self, api_client, test_base_folder, random_folder_name):
        parent_path = f"{test_base_folder}/{random_folder_name}"
        child_path = f"{parent_path}/child_folder"

        api_client.create_folder(path=parent_path)
        api_client.create_folder(path=child_path)

        # Перемещение папки в саму себя
        response = api_client.move_resource(from_path=parent_path, to_path=child_path)
        assert response.status_code in [409, 400]

    def test_move_to_self(self, api_client, test_base_folder, random_filename, test_file_content):
        file_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Перемещение файлп в себя
        response = api_client.move_resource(from_path=file_path, to_path=file_path)
        assert response.status_code in [409, 400]
