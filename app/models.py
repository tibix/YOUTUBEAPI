from app import db
import datetime as dt

# DB Classes
class Channel(db.Model):
    __tablename__           = 'channel'
    channelId               = db.Column(db.String(30), primary_key=True)
    channelTitle            = db.Column(db.String(150), nullable=False)
    channelDescription      = db.Column(db.Text, nullable=True)
    customUrl               = db.Column(db.String(255), nullable=True)
    publishedAt             = db.Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    channelThumbnailDefault = db.Column(db.Text, nullable=True)
    channelThumbnailMedium  = db.Column(db.Text, nullable=True)
    channelThumbnailHigh    = db.Column(db.Text, nullable=True)
    country                 = db.Column(db.String(3), nullable=True)
    viewCount               = db.Column(db.Integer, nullable=True)
    subscriberCount         = db.Column(db.Integer, nullable=True)
    videoCount              = db.Column(db.Integer, nullable=False)

    videos                  = db.relationship('Video', backref='cVideos', lazy=True)
    playlists               = db.relationship('Playlist', backref='playlists', lazy=True)


class Video(db.Model):
    __tablename__           = 'video'
    videoId                 = db.Column(db.String(50), primary_key=True)
    videoTitle              = db.Column(db.Text, nullable=False)
    videoDescription        = db.Column(db.Text, nullable=True)
    publishedAt             = db.Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    videoThumbnailDefault   = db.Column(db.Text, nullable=True)
    videoThumbnailMedium    = db.Column(db.Text, nullable=True)
    videoThumbnailHigh      = db.Column(db.Text, nullable=True)
    videoDuration           = db.Column(db.String(50), nullable=False)
    videoDimension          = db.Column(db.String(4), nullable=True)
    videoDefinition         = db.Column(db.String(5), nullable=True)
    viewCount               = db.Column(db.Integer, nullable=False, default=0)
    likeCount               = db.Column(db.Integer, nullable=False, default=0)
    dislikeCount            = db.Column(db.Integer, nullable=False, default=0)
    commentCount            = db.Column(db.Integer, nullable=False, default=0)
    channel                 = db.Column(db.String(200), db.ForeignKey('channel.channelId'), nullable=False)
    playlist                = db.Column(db.String(100), db.ForeignKey('playlist.playlistId'), nullable=True)
 
    comments                = db.relationship('Comment', backref='comments', lazy=True)


class Playlist(db.Model):
    __tablename__           = 'playlist'
    playlistId              = db.Column(db.String(100), primary_key=True)
    playlistItems           = db.Column(db.Text, nullable=True)
    channelId               = db.Column(db.String(200), db.ForeignKey('channel.channelId'), nullable=False)
    videoId                 = db.Column(db.String(200), db.ForeignKey('video.videoId'), nullable=False)

    videos                  = db.relationship('Video', foreign_keys=[videoId], backref='pVideos')


class Comment(db.Model):
    __tablename__           = 'comment'
    commentId               = db.Column(db.String(100), primary_key=True)
    commentInitialText      = db.Column(db.Text, nullable=True) #textOriginal
    commentFinalText        = db.Column(db.Text, nullable=False) #textDisplay
    commentBy               = db.Column(db.String(255), nullable=False)
    commentLikeCount        = db.Column(db.Integer, nullable=False, default=0)
    commentPublishedAt      = db.Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    commentUpdatedAt        = db.Column(db.DateTime(), nullable=False, default=dt.datetime.utcnow)
    commentReplyCount       = db.Column(db.Integer, nullable=False, default=0)
    parentCommentId         = db.Column(db.String(200), nullable=True)
    videoId                 = db.Column(db.String(200), db.ForeignKey('video.videoId'), nullable=False)




