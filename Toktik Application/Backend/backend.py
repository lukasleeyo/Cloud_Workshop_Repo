from uuid import uuid4
from Backend.classes import Comment
from Backend.classes import Like
from Backend.classes import Post
from Backend.database import UsersDB
from Backend.database import ContributionsDB
from Backend.database import PostsDB
from datetime import datetime
import pytz


class Backend:

    sgTimeZone = pytz.timezone("Asia/Singapore")

    # check account valid
    def hasAccount(testAccount):
        return UsersDB.checkAccount(testAccount)

    def isValidName(account, name):
        trimmed = name.strip()
        if trimmed == "":
            return False
        # see if duplicate exists
        return UsersDB.checkName(account, name)

    def getName(account):
        return UsersDB.getName(account)

    def setName(account, name):
        UsersDB.setName(account, name)

    def getWarningCount(account):
        return PostsDB.getWarningCount(account)

    def getWarnedContents(account):
        # list of Post objects
        return PostsDB.getWarnedContents(account)

    # return no of posts this user has posted
    def checkPostCount(userID):
        return ContributionsDB.checkPostCount(userID)

    # return no of likes and comments this user has made
    def checkReplyCount(userID):
        return ContributionsDB.checkReplyCount(userID)

    def hasPost(postID):
        return PostsDB.hasPost(postID)

    # create new post
    def createPost(testAccount, mediaFile, fileType):
        postID = str(uuid4())
        now = datetime.now(Backend.sgTimeZone).strftime("%d/%m/%Y %H:%M:%S")
        newPost = Post(postID=postID, userID=testAccount, dateTime=now)
        PostsDB.createPost(newPost, mediaFile, fileType)

    # delete a post
    def deletePostByPostID(postID):
        PostsDB.deletePostByPostID(postID)

    # create like
    def like(userID, postID):
        likeID = str(uuid4())
        newLike = Like(likeID=likeID, userID=userID, postID=postID)
        PostsDB.createLike(like=newLike)

    # check whether user can like post
    def canLike(userID, postID):
        return PostsDB.canLike(userID=userID, postID=postID)

    # unlike post
    def unlike(userID, postID):
        PostsDB.deleteLike(userID=userID, postID=postID)

    # Create comment by user and post and increment comment count
    def createComment(userID, postID, msg):
        commentID = str(uuid4())
        now = datetime.now(Backend.sgTimeZone).strftime("%d/%m/%Y %H:%M:%S")
        newComment = Comment(commentID=commentID, postID=postID,
                             userID=userID, dateTime=now, msg=msg)
        PostsDB.createComment(newComment)

    # get comments by postID -> return list of string comments msg only
    def getComments(postID):
        return PostsDB.getCommentsByPostID(postID)

    def getLikes(postID):
        return len(PostsDB.getLikesByPostID(postID))

    def downloadMedia(filePrefix, mediaURL):
        return PostsDB.downloadFile(filePrefix, mediaURL)

    def getNewPosts(dateTime):
        # return a list of Post objects later than dateTIme
        return PostsDB.getNewPosts(dateTime)

    def getPrevPosts(dateTime):
        # return a list of Post objects equal or less than dateTIme
        return PostsDB.getPrevPosts(dateTime)

    def censor(post):
        PostsDB.censor(post)

    def justDelete(post):
        PostsDB.justDelete(post)

    def getCensoredUsers():
        return PostsDB.getCensoredUsers()


if __name__ == "__main__":
    pass
