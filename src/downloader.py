################################################################
##### Script to download video files from index of websites ####
#####                                                       ####
#####           created by Abhijeet Vashistha               ####
################################################################

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import subprocess

def get_html(url):
    if type(url) != type(''):
        raise ValueError('String is expected in url')
    html_string = ''
    try:
        response = urlopen(url)
        html_bytes = response.read()
        html_string = html_bytes.decode('utf-8')
        return html_string
    except Exception as e:
        print('Error: Not able to find requested link ' + str(e))

def extract_links(html, base_link=None):
    html_page = BeautifulSoup(html, 'html.parser')
    all_links = html_page.find_all('a')
    video_links = []
    for link in all_links:
        href = link.get('href')
        name = link.string
        if type(href) == type('') and href.lower().endswith(('.mp4', '.mkv', '.avi', '.3gp')):
            if href.startswith(('http://', 'https://')) == False and base_link != None:
                href = base_link + href
            video_links.append({'name': name, 'link': href})
    return video_links


def main():
    link = 'http://dl.funsaber.net/serial/Mr.%20Robot/season%201/720/'
    download_folder = os.path.join(os.getenv('HOME'), 'Downloads')
    print('download folder ->', download_folder)
    html = get_html(link)
    # print(html)
    links = extract_links(html, link)
    print(links)
    if len(links) == 0:
        print('No links found')
        exit(1)
    for link in links:
        print('Downloading ->', link['name'])
        try:
            download_file = os.path.join(download_folder, link['name'])
            subprocess.call(['curl', '-o', download_file, '-O', link['link']])
        except KeyboardInterrupt:
            print('Keyboard intterupt')
            exit(0)
 
if __name__ == '__main__':
    main()
