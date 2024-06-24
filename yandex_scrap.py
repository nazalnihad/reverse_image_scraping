import json
import requests
from bs4 import BeautifulSoup
import os
import time
from requests.exceptions import RequestException

def get_img_search_url(file_path, max_retries=5):
    search_url = 'https://yandex.com/images/search'
    files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(search_url, params=params, files=files, headers=headers, verify=True, timeout=30)
            response.raise_for_status()
            
            query_string = json.loads(response.content)['blocks'][0]['params']['url']
            img_search_url = search_url + '?' + query_string + '&cbir_page=similar'
            
            return img_search_url
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(5)  # Wait for 5 seconds before retrying

def download_similar_images(img_search_url, scraped_folder, num_images, global_counter, max_retries=3):
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
                print('No similar images found.')
                return global_counter

            # Download the specified number of similar images
            for i, img in enumerate(img_tags[:num_images]):
                img_url = 'https:' + img['src']
                img_data = requests.get(img_url, headers=headers, verify=False, timeout=30).content
                with open(os.path.join(scraped_folder, f'NV_{global_counter}.jpg'), 'wb') as f:
                    f.write(img_data)
                print(f'Downloaded NV_{global_counter}.jpg')
                global_counter += 1
                time.sleep(1)  # Small delay between downloading images

            return global_counter
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(5)  # Wait for 5 seconds before retrying

def main(image_path, scraped_folder, num_images):
    if not os.path.exists(scraped_folder):
        os.makedirs(scraped_folder)

    global_counter = 1

    try:
        img_search_url = get_img_search_url(image_path)
        global_counter = download_similar_images(img_search_url, scraped_folder, num_images, global_counter)
    except Exception as e:
        print(f"Error processing image: {str(e)}")

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'  # Replace with the path to your image
    scraped_folder = 'new_scraped_images'
    num_images = 20  
    main(image_path, scraped_folder, num_images)
