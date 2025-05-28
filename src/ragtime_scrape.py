import requests as re
from bs4 import BeautifulSoup
import time
import os
import sys


def main(start_page=1, end_page=9):
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }
    def scrape_page(url, headers=HEADERS, delay=5):
        response = re.get(url, headers=headers)
        if response.status_code == 200:
            time.sleep(delay)
            return response
        else:
            print(f'Request unsuccessful:{response.status_code}')
            time.sleep(delay)

    def get_midi_paths(url, headers=HEADERS):
        base_midi_path = 'https://www.ragtimemusic.com/{x}'
        midi_paths = []
        response = scrape_page(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            link_text = link.get('href')
            if link_text and '.mid' in link_text:
                midi_paths.append(base_midi_path.format(x=link_text))
        return midi_paths


    def download_midis(midi_paths, delay=5):
        print('Downloading MIDI files')
        n = len(midi_paths)
        counter = 1
        for m in midi_paths:
            print(f'{counter}/{n} files downloading')
            response = scrape_page(m, delay=delay)
            if response.status_code == 200:
                if not os.path.exists(m.split('/')[-1]):
                    with open(m.split('/')[-1], "wb") as f:
                        f.write(response.content)
                    print("MIDI file downloaded successfully.")
                else:
                    print("MIDI file already exists, skipping")
            else:
                print(f"Failed to download file: Status code {response.status_code}")
            counter += 1

    def download_ragtime_midis(start_page=start_page, end_page=end_page):
        base_meta_path = 'https://www.ragtimemusic.com/title{x}.html#top%20of%20page'
        all_midi_paths = []
        print('Getting MIDI urls...')
        for i in range(start_page, end_page):
            print(f'{start_page - i}/{end_page - start_page + 1} pages...')
            all_midi_paths += get_midi_paths(base_meta_path.format(x=i))
        print('Done')
        download_midis(all_midi_paths)


    download_ragtime_midis()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        main(1, 9)
    else:
        main(int(sys.argv[1]), int(sys.argv[2]))

