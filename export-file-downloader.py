import os
import json
from urllib.parse import urlparse

# load the export directory
export_directory = os.getenv("EXPORT_DIRECTORY")

# Function to download a file from a given URL
def download_file(url, local_filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {local_filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")

# Function to extract file name with extension from URL
def get_filename_from_url(url, default_name):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    return file_name if file_name else default_name

# Function to process the JSON export file and download referenced files
def process_export_file(export_file_path, download_dir):
    # Ensure the download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Open and read the JSON file
    with open(export_file_path, 'r') as file:
        data = json.load(file)
    
    # Debug: print the loaded JSON data (first 1000 characters for brevity)
    print(f"Loaded JSON data: {str(data)[:1000]}")
    
    # Iterate through the JSON data to find file URLs
    for record in data:
        if 'files' in record:
            for file_info in record['files']:
                if 'url_private_download' in file_info:
                    url = file_info['url_private_download']
                    filename = get_filename_from_url(url, file_info.get('name', 'unknown_file'))
                    local_filename = os.path.join(download_dir, filename)
                    
                    # Debug: print the URL and the intended local filename
                    print(f"Downloading {url} to {local_filename}")
                    
                    # Download the file
                    download_file(url, local_filename)
                else:
                    print("No 'url_private_download' field found in file_info.")
        else:
            print("No 'files' field found in record.")

if __name__ == "__main__":
    # Path to the Slack export JSON file
    
    # Directory to save downloaded files
    download_dir = 'downloaded_files'
    
    # Process the export file and download files
    process_export_file(export_directory, download_dir)