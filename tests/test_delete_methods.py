import time

import pytest


class TestDeleteMethods:

    def test_delete_file_to_trash(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка файла
        path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Удаление
        response = api_client.delete_resource(path=path, permanently=False)
        assert response.status_code in [204, 200, 202]

        # Проверка остутсвия в списке
        resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in resources["_embedded"]["items"]]
        assert random_filename not in items

    def test_delete_nested_file(self, api_client, test_base_folder, random_folder_name, random_filename,test_file_content):
        # Создание папки
        folder_path = f"{test_base_folder}/{random_folder_name}"
        api_client.create_folder(path=folder_path)

        # Загрузка файла в папку
        file_path = f"{folder_path}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Удаление только файла
        response = api_client.delete_resource(path=file_path, permanently=False)
        assert response.status_code in [204, 200, 202]

        # Проверка, что папка осталась
        resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in resources["_embedded"]["items"]]
        assert random_folder_name in items

        # Проверка отсутствия файла в папке
        folder_resources = api_client.get_resources(path=folder_path)
        folder_items = [item["name"] for item in folder_resources["_embedded"]["items"]]
        assert random_filename not in folder_items

    def test_delete_folder(self, api_client, test_base_folder, random_folder_name):
        # Создание папки
        path = f"{test_base_folder}/{random_folder_name}"
        api_client.create_folder(path=path)

        # Удаление папки
        response = api_client.delete_resource(path=path, permanently=False)
        assert response.status_code in [204, 200, 202]

        # Проверка остутсвия
        resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in resources["_embedded"]["items"]]
        assert random_folder_name not in items

    def test_delete_folder_with_content(self, api_client, test_base_folder, random_folder_name, random_filename,test_file_content):
        # Создание папки
        folder_path = f"{test_base_folder}/{random_folder_name}"
        api_client.create_folder(path=folder_path)

        # Загрузка файла в папку
        file_path = f"{folder_path}/{random_filename}"
        upload_url = api_client.get_upload_url(path=file_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Удаление папки (содержимое должно удалиться вместе с папкой)
        response = api_client.delete_resource(path=folder_path, permanently=False)
        assert response.status_code in [204, 200, 202]

        time.sleep(1)

        # Проверка отсутствия папки
        resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in resources["_embedded"]["items"]]
        assert random_folder_name not in items

    def test_delete_nonexistent_resource(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/nonexistent_{random_filename}"
        response = api_client.delete_resource(path=path)
        assert response.status_code in [404, 409]

    def test_delete_already_deleted_resource(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка и первое удаление файла
        path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())
        api_client.delete_resource(path=path, permanently=False)

        # Повторное удаление
        response = api_client.delete_resource(path=path, permanently=False)
        assert response.status_code in [404, 409]

    def test_delete_with_invalid_path(self, api_client, test_base_folder):
        invalid_path = f"{test_base_folder}/invalid:name"
        response = api_client.delete_resource(path=invalid_path)
        assert response.status_code in [400, 404]

    def test_delete_root_disk(self, api_client):
        response = api_client.delete_resource(path="/", permanently=True)
        assert response.status_code in [400, 403, 409]
