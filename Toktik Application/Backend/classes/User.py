class User(object):
    def __init__(self, userID, name, likesCount, commentsCount, postsCount):
        self.userID = userID
        self.name = name
        self.likesCount = likesCount
        self.commentsCount = commentsCount
        self.postsCount = postsCount

    def to_dict(self):
        data = {
            u'userID': self.userID,
            u'name': self.name,
            u'likesCount': self.likesCount,
            u'commentsCount': self.commentsCount,
            u'postsCount': self.postsCount
        }
        return data
