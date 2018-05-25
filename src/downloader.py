################################################################
##### Script to download video files from index of websites ####
#####                                                       ####
#####           created by Abhijeet Vashistha               ####
################################################################

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import subprocess
import sys

def get_html(url):
    '''Function for returning html content of the url as string'''
    if type(url) != type(''):
        raise ValueError('String is expected in url')
    html_string = ''
    try:
        response = urlopen(url)
        html_bytes = response.read()
        html_string = html_bytes.decode('utf-8')
        return html_string
    except Exception as err:
        print('Error: Not able to find requested link ' + str(err))
        exit(1)

def extract_links(html, base_link=None):
    '''Function to extract the links from html page'''
    html_page = BeautifulSoup(html, 'html.parser')
    all_links = html_page.find_all('a')
    video_links = []
    for link in all_links:
        href = link.get('href')
        name = link.string
        if type(href) == type('') and href.lower().endswith(('.mp4', '.mkv', '.avi', '.3gp', '.flv', '.wmv', '.mov')): #check if the link points to a video file
            if href.startswith(('http://', 'https://')) == False and base_link != None: 
                href = base_link + href # if relative links are used then make absolute link
            video_links.append({'name': name, 'link': href})
    video_links.sort(key=lambda k: k['name'])
    return video_links


def main():
    page_link = sys.argv[1]
    print('Extracting download links from ->', page_link)
    html = get_html(page_link)
    # print(html)
    links = extract_links(html, page_link)
    if len(links) == 0:
        print('No links found')
        exit(0)
    else:
        print('Found links ->', links)
    download_folder = os.path.join(os.getenv('HOME'), 'Downloads')
    print('Download folder ->', download_folder)
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
