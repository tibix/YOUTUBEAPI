import json
from flask import render_template, url_for, request, Response, Blueprint, redirect
from markupsafe import escape
from datetime import datetime as dt
from app.yt_stats import YTSearch, YTStats
from app.dirty_secrets import SEARCH_API_KEY
from app.models import Channel, Video
from pprint import pprint
from app import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@main.route("/index")
def index():
    with open('oneflash_test.json', 'r') as json_file:
        data = json.load(json_file)
    return render_template('index.html', data=data)

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/search", methods=["POST"])
def search():
    search_term = request.form['search']
    search = YTSearch(SEARCH_API_KEY, search_term)
    data = search.get_channels()
    return render_template('search.html', data=data)


@main.route("/channels")
def channels():
    channels = Channel.query.all()
    return render_template('channels.html', channels=channels)

@main.route("/channel/<channel>")
def view_channel(channel):
    data = Channel.query.filter_by(channelId=channel).first_or_404()
    return render_template('channel.html', data=data)


@main.route("/analyze_channel/<channel>")
def analyze_channel(channel):
    channel_details = YTStats(SEARCH_API_KEY, channel)
    
    if Channel.query.filter_by(channelId=channel).first() is not None: 
        data = Channel.query.filter_by(channelId=channel).first_or_404()
        return redirect(url_for('main.view_channel', channel=channel))
    else:
        data = channel_details.get_channel_details()
        pprint(data)
        channel_data = Channel(
            channelId               = data['channelId'],
            channelTitle            = data['channelTitle'],
            channelDescription      = data['channelDescription'],
            customUrl               = data['customUrl'],
            publishedAt             = data['publishedAt'],
            channelThumbnailDefault = data['channelThumbnailDefault'],
            channelThumbnailMedium  = data['channelThumbnailMedium'],
            channelThumbnailHigh    = data['channelThumbnailHigh'],
            country                 = data['country'],
            viewCount               = int(data['viewCount']),
            subscriberCount         = data['subscriberCount'],
            videoCount              = data['videoCount']
        )

        db.session.add(channel_data)
        db.session.commit()
        
        current_channel = Channel.query.filter_by(channelId=channel).first()

        if len(list(current_channel.videos)) < 1:
            videos = channel_details.get_channel_video_data()
            for video in videos:
                item = Video(
                    videoId                = video,
                    videoTitle             = videos[video]['title'],
                    videoDescription       = videos[video]['description'],
                    publishedAt            = dt.fromisoformat(videos[video]['publishedAt'][:-1]),
                    videoThumbnailDefault  = videos[video]['thumbnailDefault'],
                    videoThumbnailMedium   = videos[video]['thumbnailMedium'],
                    videoThumbnailHigh     = videos[video]['thumbnailHigh'],
                    videoDuration          = videos[video]['duration'][2:],
                    videoDimension         = videos[video]['dimension'],
                    videoDefinition        = videos[video]['definition'],
                    likeCount              = videos[video]['viewCount'],
                    commentCount           = videos[video]['commentCount'],
                    channel                = videos[video]['channelId']
                )
                db.session.add(item)
                db.session.commit()
        
        return render_template('analyze_channel.html', channel=current_channel)
   

@main.route("/videos")
def get_videos():
    return render_template('videos.html', video=videos)