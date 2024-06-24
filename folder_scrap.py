import json
import requests
from bs4 import BeautifulSoup
import os
import glob
import time
from requests.exceptions import RequestException

def get_img_search_url(file_path, max_retries=3):
    search_url = 'https://yandex.com/images/search'
    files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(search_url, params=params, files=files, headers=headers, verify=False, timeout=30)
            response.raise_for_status()
            
            query_string = json.loads(response.content)['blocks'][0]['params']['url']
            img_search_url = search_url + '?' + query_string + '&cbir_page=similar'
            
            return img_search_url
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(5)  # Wait for 5 seconds before retrying

def download_similar_images(img_search_url, save_path, reference_img_name, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(img_search_url, headers=headers, verify=False, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            img_tags = soup.find_all('img', class_='serp-item__thumb')

            if not img_tags:
                print(f'No similar images found for {reference_img_name}.')
                return

            # Create a subfolder for each reference image
            img_save_path = os.path.join(save_path, os.path.splitext(reference_img_name)[0])
            os.makedirs(img_save_path, exist_ok=True)

            # Download the first 20 similar images
            for i, img in enumerate(img_tags[:20], start=1):
                img_url = 'https:' + img['src']
                img_data = requests.get(img_url, headers=headers, verify=False, timeout=30).content
                img_filename = f'similar_{i}.jpg'
                with open(os.path.join(img_save_path, img_filename), 'wb') as f:
                    f.write(img_data)
                print(f'Downloaded {img_filename} for {reference_img_name}')
                time.sleep(1)  # Small delay between downloading images

            return
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed for {reference_img_name}: {str(e)}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(5)  # Wait for 5 seconds before retrying

def main(reference_folder, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    image_files = glob.glob(os.path.join(reference_folder, '*.jpg'))

    for image_path in image_files:
        reference_img_name = os.path.basename(image_path)
        print(f'Processing image: {reference_img_name}')
        
        try:
            img_search_url = get_img_search_url(image_path)
            download_similar_images(img_search_url, save_path, reference_img_name)
        except Exception as e:
            print(f"Error processing image {reference_img_name}: {str(e)}")
        
        time.sleep(5)  # Wait for 5 seconds between processing each image

if __name__ == '__main__':
    reference_folder = 'D:/projects/iist/backup_data/final_data/predictions/data/val/references'
    save_path = 'D:/projects/iist/backup_data/final_data/predictions/data/val/references/similar'
    main(reference_folder, save_path)