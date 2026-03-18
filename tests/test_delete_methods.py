import pytest


class TestDeleteMethods:

    def test_delete_file_to_trash(self, api_client, test_base_folder, random_filename, test_file_content):
        # Загрузка файла
        path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # 2 Удаление
        response = api_client.delete_resource(path=path, permanently=False)
        assert response.status_code in [204, 200, 202]

        # Проверка остутсвия в списке
        resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in resources["_embedded"]["items"]]
        assert random_filename not in items

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

    def test_delete_nonexistent_resource(self, api_client, test_base_folder, random_filename):
        path = f"{test_base_folder}/nonexistent_{random_filename}"
        response = api_client.delete_resource(path=path)
        assert response.status_code in [404, 409]
