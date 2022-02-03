class Comment(object):
    def __init__(self, commentID, postID, userID, msg, dateTime):
        self.commentID = commentID
        self.postID = postID
        self.userID = userID
        self.msg = msg
        self.dateTime = dateTime

    def to_dict(self):
        data = {
            u'postID': self.postID,
            u'userID': self.userID,
            u'commentID': self.commentID,
            u'dateTime': self.dateTime,
            u'msg': self.msg
        }
        return data
