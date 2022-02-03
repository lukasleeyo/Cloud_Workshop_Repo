class Like(object):
    def __init__(self, likeID, postID, userID):
        self.likeID = likeID
        self.postID = postID
        self.userID = userID

    def to_dict(self):
        data = {
            u'postID': self.postID,
            u'userID': self.userID,
            u'likeID': self.likeID
        }
        return data
