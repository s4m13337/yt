import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import subprocess

cookies = {
        'SOCS': 'CAESFggDEgk1NjYzNzYzMDUaBWVuLUdCIAEaBgiA7KioBg'
    }

def getTrendingVideos():
    url = "https://www.youtube.com/feed/trending"
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    script_tags = soup.find_all('script');
    content = []
    for tag in script_tags:
        if "var ytInitialData" in tag.text:
            content = tag.text[20:-1]   # Indexing to remove variable assignment and semicolon at end
            break

    content = json.loads(content)

    videos = (content['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]
    ['tabRenderer']['content']['sectionListRenderer']['contents'][3]
    ['itemSectionRenderer']['contents'][0]
    ['shelfRenderer']['content']['expandedShelfContentsRenderer']['items'])

    video_dict = []
    for video in videos:
        video_dict.append({
            'videoId': video['videoRenderer']['videoId'],
            'title': video['videoRenderer']['title']['runs'][0]['text'],
            'thumbnail': video['videoRenderer']['thumbnail']['thumbnails'][0]['url']
        })
    
    return video_dict


def getSearchResults(query):
    baseURL = "https://www.youtube.com/results"
    params = {'search_query' : query}
    url = baseURL + '?' + urllib.parse.urlencode(params)
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    script_tags = soup.find_all('script');
    content = []
    for tag in script_tags:
        if "var ytInitialData" in tag.text:
            content = tag.text[20:-1]   # Indexing to remove variable assignment and semicolon at end
            break

    content = json.loads(content)
    videos = (content['contents']['twoColumnSearchResultsRenderer']['primaryContents']
        ['sectionListRenderer']['contents'][0]
        ['itemSectionRenderer']['contents'])

    video_dict = []
    channel_dict = []
    for video in videos:
        
        # Collect channels 
        if 'channelRenderer' in video:
            channel_dict.append({
                'channelId': video['channelRenderer']['channelId'],
                'title': video['channelRenderer']['title']['simpleText'],
                'thumbnail': video['channelRenderer']['thumbnail']['thumbnails'][0]['url'],
                'endpoint': video['channelRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
            })

        # Collect videos
        if 'videoRenderer' in video:
            video_dict.append({
                'videoId': video['videoRenderer']['videoId'],
                'title': video['videoRenderer']['title']['runs'][0]['text'],
                'thumbnail': video['videoRenderer']['thumbnail']['thumbnails'][0]['url'],
                'duration':  video['videoRenderer']['lengthText']['simpleText'],
                'creator': video['videoRenderer']['ownerText']['runs'][0]['text']
            })
        

    return {'channels': channel_dict, 'videos': video_dict}

def grabVideoLink(videoId):
    youtubeURL = "https://www.youtube.com/watch?v=" + videoId
    result = subprocess.run(["yt-dlp", "-f", "mp4", "--get-url", youtubeURL], capture_output=True, text=True)
    return result.stdout