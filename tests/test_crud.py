import pytest
import requests


class TestCRUDWorkflow:

    def test_full_file_lifecycle(self, api_client, test_base_folder, random_filename, test_file_content):
        #  CREATE
        upload_path = f"{test_base_folder}/{random_filename}"
        upload_url = api_client.get_upload_url(path=upload_path, overwrite=True)
        api_client.upload_file(upload_url, test_file_content.encode())

        # Проверка наличия файла
        resources = api_client.get_resources(path=test_base_folder)
        assert any(item["name"] == random_filename for item in resources["_embedded"]["items"])

        # (READ)
        download_url = api_client.get_download_url(path=upload_path)
        downloaded_content = requests.get(download_url).text
        assert test_file_content in downloaded_content

        # (UPDATE)
        # Копирование файла
        copy_path = f"{test_base_folder}/copy_{random_filename}"
        copy_response = api_client.copy_resource(from_path=upload_path, to_path=copy_path)
        assert copy_response.status_code in [201, 202]

        # Перемещение в подпапку
        subfolder = f"{test_base_folder}/workflow_subfolder"
        api_client.create_folder(path=subfolder)
        moved_path = f"{subfolder}/{random_filename}"
        move_response = api_client.move_resource(from_path=upload_path, to_path=moved_path)
        assert move_response.status_code in [201, 202]

        # (DELETE) -
        delete_copy = api_client.delete_resource(path=copy_path, permanently=True)
        assert delete_copy.status_code in [200, 202, 204]

        delete_moved = api_client.delete_resource(path=moved_path, permanently=True)
        assert delete_moved.status_code in [200, 202, 204]

        delete_folder = api_client.delete_resource(path=subfolder, permanently=True)
        assert delete_folder.status_code in [200, 202, 204]

        # Проверка удаления
        final_resources = api_client.get_resources(path=test_base_folder)
        items = [item["name"] for item in final_resources["_embedded"]["items"]]
        assert random_filename not in items
        assert f"copy_{random_filename}" not in items
        assert "workflow_subfolder" not in items
