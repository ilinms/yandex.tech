import pytest


class TestPutMethods:

    def test_create_folder(self, api_client, test_base_folder, random_folder_name):
        path = f"{test_base_folder}/{random_folder_name}"
        response = api_client.create_folder(path=path)
        assert response.status_code in [201, 409]

    def test_create_nested_folder(self, api_client, test_base_folder, random_folder_name):
        parent_path = f"{test_base_folder}/{random_folder_name}"
        nested_path = f"{parent_path}/nested"

        api_client.create_folder(path=parent_path)
        response = api_client.create_folder(path=nested_path)
        assert response.status_code in [201, 409]

    def test_create_long_folder_name(self, api_client, test_base_folder):
        long_name = "a" * 1000
        path = f"{test_base_folder}/{long_name}"
        response = api_client.create_folder(path=path)
        assert response.status_code in [400, 404, 409]

    def test_create_folder_empty_name(self, api_client, test_base_folder):
        path = f"{test_base_folder}/"
        response = api_client.create_folder(path=path)
        assert response.status_code in [400, 404, 409]

