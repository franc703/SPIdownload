import requests
from bs4 import BeautifulSoup
import os

def download_file(url, save_path):
    """ Helper function to download a file from a given URL to a specified save path """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def get_nc_files(url):
    """ Scrape the directory page for .nc file links """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.nc')]
    return links

def main():
    base_url = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DROUGHTOBS/Drought_Observatories_datasets/GDO_ERA5_Standardized_Precipitation_Index_SPI3/ver1-0-0"
    save_directory = "./spi_nc_files"  # Directory where files will be saved
    
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    file_urls = get_nc_files(base_url)
    
    for file_url in file_urls:
        filename = file_url.split('/')[-1]
        save_path = os.path.join(save_directory, filename)
        
        try:
            print(f"Downloading {filename}...")
            download_file(file_url, save_path)
            print(f"Downloaded {filename} successfully.")
        except requests.exceptions.HTTPError as e:
            print(f"Failed to download {filename}. Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
