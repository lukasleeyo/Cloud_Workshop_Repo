class Post(object):
    def __init__(self, postID, userID, dateTime, mediaURL="", mediaType="", likesCount=0, commentsCount=0):
        self.postID = postID
        self.userID = userID
        self.mediaURL = mediaURL
        self.mediaType = mediaType
        self.dateTime = dateTime
        self.likesCount = likesCount
        self.commentsCount = commentsCount

    def to_dict(self):
        data = {
            u'postID': self.postID,
            u'userID': self.userID,
            u'mediaURL': self.mediaURL,
            u'mediaType': self.mediaType,
            u'dateTime': self.dateTime,
            u'likesCount': self.likesCount,
            u'commentsCount': self.commentsCount
        }
        return data
