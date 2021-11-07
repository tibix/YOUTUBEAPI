import requests
import json
from tqdm import tqdm
from datetime import datetime as dt
from pprint import pprint

class YTStats:
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None


    def get_channel_details(self):
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet&part=statistics&id={self.channel_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        errors = []

        try:
            data = data['items'][0]
        except KeyError as e:
            return f"Cannot read data: {e}"
        
        try:
            channelId = data['id']
        except:
            errors.append("Cannot read channelId")
        
        try:
            channelTitle = data['snippet']['title']
        except:
            errors.append("Cannot read title")
        
        try:
            channelDescription = data['snippet']['description']
        except:
            errors.append("Cannot read description")

        try:
            customUrl = data['snippet']['customUrl']
        except:
            customUrl = None

        try:
            publishedAt = dt.fromisoformat(data['snippet']['publishedAt'][:-1])
        except:
            errors.append("Cannot read publishedAt")
        
        try:
            channelThumbnailDefault = data['snippet']['thumbnails']['default']['url']
        except:
            errors.append("Cannot read default thumbnail URL")

        try:
            channelThumbnailMedium = data['snippet']['thumbnails']['medium']['url']
        except:
            errors.append("Cannot read medium thumbnail URL")

        try:
            channelThumbnailHigh = data['snippet']['thumbnails']['high']['url']
        except:
            errors.append("Cannot read high thumbnail URL")
        
        try:
            country = data['snippet']['country']
        except:
            country = None

        try:
            viewCount = data['statistics']['viewCount']
        except:
            errors.append("Cannot read viewsCount")

        try:
            subscriberCount = int(data['statistics']['subscriberCount'])
        except:
            errors.append("Cannot read subscriberCount")
        
        try:
            videoCount = int(data['statistics']['videoCount'])
        except:
            errors.append("Cannot read videoCount")

        if len(errors) < 1:
            # create the dictionary, populate with values and return it
            channel_details = dict()

            channel_details['channelId'] = channelId
            channel_details['channelTitle'] = channelTitle
            channel_details['channelDescription'] = channelDescription
            channel_details['customUrl'] = customUrl
            channel_details['publishedAt'] = publishedAt
            channel_details['channelThumbnailDefault'] = channelThumbnailDefault
            channel_details['channelThumbnailMedium'] = channelThumbnailMedium
            channel_details['channelThumbnailHigh'] = channelThumbnailHigh
            channel_details['country'] = country
            channel_details['viewCount'] = viewCount
            channel_details['subscriberCount'] = subscriberCount
            channel_details['videoCount'] = videoCount

            return channel_details
        else:
            # return an error
            return errors


    def get_channel_video_data(self):
        channel_videos = self._get_channel_videos(limit=50)

        for video_id in tqdm(channel_videos):
                data = self._get_single_video_data(video_id)
                # from data['snippet'] get:
                    # - ['title]
                    # - ['description']
                    # - ['publishedAt]
                    # - [thumbnails]:
                        # - ['default']['url']
                        # - ['medium']['url']
                        # - ['high']['url']
                        # - ['maxres']['url']
                # from data['contentDetails'] get:
                    # - ['duration']
                    # - ['dimension']
                    # - ['definition']
                # from data['statistics'] get:
                    # - ['viewCount']
                    # - ['likeCount']
                    # - ['dislikeCount']
                    # - ['commentCount']
                channel_videos[video_id]['videoId'] = video_id
                channel_videos[video_id]['title'] = data['snippet']['title']
                channel_videos[video_id]['description'] = data['snippet']['description']
                channel_videos[video_id]['publishedAt'] = data['snippet']['publishedAt']
                channel_videos[video_id]['thumbnailDefault'] = data['snippet']['thumbnails']['default']['url']
                channel_videos[video_id]['thumbnailMedium'] = data['snippet']['thumbnails']['medium']['url']
                channel_videos[video_id]['thumbnailHigh'] = data['snippet']['thumbnails']['high']['url']
                channel_videos[video_id]['duration'] = data['contentDetails']['duration']
                channel_videos[video_id]['dimension'] = data['contentDetails']['dimension']
                channel_videos[video_id]['definition'] = data['contentDetails']['definition']
                channel_videos[video_id]['viewCount'] = data['statistics']['viewCount']
                channel_videos[video_id]['likeCount'] = data['statistics']['likeCount']
                channel_videos[video_id]['dislikeCount'] = data['statistics']['dislikeCount']
                channel_videos[video_id]['commentCount'] = data['statistics']['commentCount']
                channel_videos[video_id]['channelId'] = data['snippet']['channelId']
        self.video_data = channel_videos
        return channel_videos


    def _get_single_video_data(self, video_id):
        url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&part=contentDetails&part=statistics&id={video_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0]
        except:
            print('error getting single video data')
            data = dict()
        
        return data


    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id'
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        
        vid, npt = self._get_channel_videos_per_page(url)
        idx = 0
        while(npt is not None and idx < 10):
            next_url = url + "&pageToken=" + npt
            next_video, npt = self._get_channel_videos_per_page(next_url)
            vid.update(next_video)
            idx += 1
        return vid


    def _get_channel_videos_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        if 'items' not in data:
            return channel_videos, None

        item_data = data['items']
        nextPageToken = data.get("nextPageToken", None)

        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError:
                print("error")
        
        return channel_videos, nextPageToken

    # def get_channel_statistics(self):
    #     url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
    #     # print(url)
    #     json_url = requests.get(url)
    #     data  = json.loads(json_url.text)
    #     # print(data)
    #     try:
    #         data = data['items'][0]['statistics']
    #     except:
    #         data = None
        
    #     self.channel_statistics = data
    #     return data
    
    # def dump(self):
    #     if self.channel_statistics is None or self.video_data is None:
    #         print('No data available')
    #         return
        
    #     fused_data = {self.channel_id: {"channel_statistics":self.channel_statistics, "video_data": self.video_data}}
    #     channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
    #     channel_title = channel_title.replace(" ", "_").lower()
    #     file_name = channel_title + ".json"
    #     with open(file_name, 'w') as f:
    #         json.dump(fused_data, f, indent=4)
        
    #     print('File dumped')


class YTSearch:
    def __init__(self, api_key, search):
        self.api_key = api_key
        self.search = search
        self.url = f'https://www.googleapis.com/youtube/v3/search?q={self.search}&type=channel&part=snippet&order=videoCount&maxResults=10&key={self.api_key}'


    def get_channels(self):
        channels = dict()
        json_url = requests.get(self.url)
        data = json.loads(json_url.text)
        item_data = data['items']
        for item in item_data:
            channelId = item['id']['channelId']
            channels[channelId] = dict()
            channels[channelId].update(
                {"id": channelId,
                 "title": item['snippet']['title'],
                 "thumbnail":item['snippet']['thumbnails']['medium']['url'],
                 "url": "https://youtube.com/channel/" + item['id']['channelId']}
            )
        return channels