import requests
import os

def download_files_by_extension(repo_url, file_extension, destination_file_path, access_token):
    headers = {'Authorization': f'token {access_token}'}
    
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith(file_extension):
                download_file(item['download_url'], destination_file_path)
            elif item['type'] == 'dir':
                repo_url = item['url']
                download_files_by_extension(repo_url, file_extension, destination_file_path, access_token)
    else:
        print("Failed to retrieve repository contents.")

def download_file(url, destination_file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination_file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully: {destination_file_path}")
    else:
        print(f"Failed to download the file: {url}")


