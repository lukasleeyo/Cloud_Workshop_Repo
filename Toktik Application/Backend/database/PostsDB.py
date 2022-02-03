from google.cloud import firestore_v1
from Backend.initGCP import InitGCP
from uuid import uuid4
from Backend.classes import Post
from Backend.classes import Comment
from Backend.classes import Like
from Backend.database import ContributionsDB
from Backend.database import UsersDB
import operator

# Initialize to GCP
GCP_DB = InitGCP.initDB()
GCP_STORAGE = InitGCP.initStorage()


class PostsDB:
    # upload media and returns the URL of the media stored in GCP Storage
    def uploadFile(userID, file, contentType):
        try:
            bucketName = "dscworkshopbucket"
            fileType = contentType.split("/")[1]

            uuid = uuid4()
            destFileName = "{0}/{1}.{2}".format(userID, uuid, fileType)  # jpeg

            bucket = GCP_STORAGE.bucket(bucketName)
            blob = bucket.blob(destFileName)

            blob.upload_from_filename(
                file, content_type=contentType)  # image/jpeg

            # print("File {} uploaded to {}.".format(file, destFileName))

            mediaURL = "https://storage.cloud.google.com/{0}/{1}/{2}.{3}?authuser=0".format(
                bucketName, userID, uuid, fileType)  # jpeg

            return mediaURL
        except:
            print("upload_media_error")
            return "upload_media_error"

    # download media from URL

    def downloadFile(filePrefix, mediaURL):
        try:
            bucketName = "dscworkshopbucket"
            bucket = GCP_STORAGE.bucket(bucketName)
            front = "https://storage.cloud.google.com/dscworkshopbucket/"
            back = "?authuser=0"
            sourceFileName = mediaURL.replace(front, "").replace(back, "")
            blob = bucket.blob(sourceFileName)
            destFileName = filePrefix + sourceFileName.split(".")[-1]
            blob.download_to_filename(destFileName)
            return destFileName
        except:
            print("download_media_error")
            return "download_media_error"

    # update post count by user id
    def updatePostsCountByUserID(userID):
        try:
            users_ref = GCP_DB.collection(u'Users').document(userID)
            postsCount = ContributionsDB.checkPostCount(userID)
            users_ref.update({u'postsCount': postsCount})
        except:
            print("update_posts_count_error")
            return "update_posts_count_error"

    # create post with mphoto/video
    def createPost(post: Post, file, fileType):
        try:
            mediaURL = PostsDB.uploadFile(post.userID, file, fileType)
            post.mediaURL = mediaURL
            post.mediaType = fileType
            GCP_DB.collection(u'Posts').document(
                post.postID).set(post.to_dict())
            PostsDB.updatePostsCountByUserID(post.userID)
        except:
            print("error_create_post")
            return "error_create_post"

    def hasPost(postID):
        posts_ref = GCP_DB.collection(u'Posts').where(
            u'postID', u'==', postID).get()
        return bool(posts_ref)

    # get post by postID
    def getPostByID(postID):
        try:
            # Create a reference to the Posts collection
            posts_ref = GCP_DB.collection(u'Posts')
            # Create a query against the collection
            query_ref = posts_ref.where(u'postID', u'==', postID).get()
            for doc in query_ref:
                docDict = doc.to_dict()
                return Post(docDict['postID'], docDict['userID'], docDict['dateTime'],
                            docDict['mediaURL'], docDict['mediaType'], docDict['likesCount'], docDict['commentsCount'])
        except:
            print("get_post_error")
            return "get_post_error"

    # update likes count by postID
    # if canLike is True, increment likes. otherwise decrement likes

    def updateLikesCountByPostID(postID, canLike=True):
        try:
            # Create a reference to the Posts collection
            posts_ref = GCP_DB.collection(u'Posts').document(postID)

            post = PostsDB.getPostByID(postID)
            if canLike:
                post.likesCount += 1
            else:
                post.likesCount -= 1

            # update likes count in database
            posts_ref.update({u'likesCount': post.likesCount})
        except:
            print("update_like_error")
            return "update_like_error"

    # update like count by user id

    def updateLikesCountByUserID(userID, canLike=True):
        try:
            users_ref = GCP_DB.collection(u'Users').document(userID)
            likesCount = ContributionsDB.checkLikesCount(userID)

            users_ref.update({u'likesCount': likesCount})
        except:
            print("update_likes_count_error")
            return "update_likes_count_error"

    # create likes if canLike is True, otherwise delete the like record
    def createLike(like: Like):
        try:
            GCP_DB.collection(u'Likes').document(
                like.likeID).set(like.to_dict())
            PostsDB.updateLikesCountByPostID(postID=like.postID, canLike=True)
            PostsDB.updateLikesCountByUserID(like.userID, True)
        except:
            print("create_like_error")
            return "create_like_error"

    # check whether user can like a post

    def canLike(userID, postID):
        try:
            records = []
            likes_ref = GCP_DB.collection(u'Likes').where(
                u'postID', u'==', postID).where(u'userID', u'==', userID).get()
            for doc in likes_ref:
                records.append(doc.to_dict()["userID"])

            return len(records) == 0  # return true if user can like post
        except:
            print("can_like_error")
            return "can_like_error"

    # delete like record

    def deleteLike(userID, postID):
        try:
            likeID = ""
            likes_ref = GCP_DB.collection(u'Likes').where(
                u'postID', u'==', postID).where(u'userID', u'==', userID).get()
            for doc in likes_ref:
                likeID = doc.to_dict()["likeID"]

            GCP_DB.collection(u'Likes').document(likeID).delete()
            PostsDB.updateLikesCountByPostID(postID=postID, canLike=False)
            PostsDB.updateLikesCountByUserID(userID, False)
        except:
            print("delete_like_error")
            return "delete_like_error"

    # get all likes by postID

    def getLikesByPostID(postID):
        try:
            likes = []
            likes_ref = GCP_DB.collection(u'Likes').where(
                u'postID', u'==', postID).get()

            for doc in likes_ref:
                docDict = doc.to_dict()
                like = Like(
                    postID=docDict["postID"], userID=docDict["userID"], likeID=docDict["likeID"])
                likes.append(like)

            return likes
        except:
            print("get_likes_by_postid_error")
            return "get_likes_by_postid_error"

    # update comments count by postID

    def updateCommentsCountByPostID(postID):
        try:
            # Create a reference to the Posts collection
            posts_ref = GCP_DB.collection(u'Posts').document(postID)

            post = PostsDB.getPostByID(postID)
            post.commentsCount += 1

            # update comments count in database
            posts_ref.update({u'commentsCount': post.commentsCount})
        except:
            print("update_comment_error")
            return "update_comment_error"

    # update comment count by user id

    def updateCommentsCountByUserID(userID):
        try:
            users_ref = GCP_DB.collection(u'Users').document(userID)
            commentsCount = ContributionsDB.checkCommentsCount(userID)

            users_ref.update({u'commentsCount': commentsCount})
        except:
            print("update_comments_count_error")
            return "update_comments_count_error"

    # create comment
    def createComment(comment: Comment):
        try:
            result = GCP_DB.collection(u'Comments').document(
                comment.commentID).set(comment.to_dict())
            # increment comment count by post ID
            PostsDB.updateCommentsCountByPostID(comment.postID)
            PostsDB.updateCommentsCountByUserID(comment.userID)
        except:
            print("create_comment_error")
            # print(traceback.print_exc())
            return "create_comment_error"

    # get comments by postID -> returns list of string comment message

    def getCommentsByPostID(postID):
        try:
            comments = []
            comments_ref = GCP_DB.collection(u'Comments').where(
                u'postID', u'==', postID).get()

            for doc in comments_ref:
                docDict = doc.to_dict()
                comment = Comment(msg=docDict["msg"], commentID=docDict["commentID"],
                                  postID=docDict["postID"], userID=docDict["userID"], dateTime=docDict["dateTime"])
                comments.append(comment)

            # sort comments by latest datetime
            sortedComments = sorted(
                comments, key=operator.attrgetter("dateTime"))

            commentMsgs = []

            for comment in sortedComments:
                commentMsgs.append(comment)

            return commentMsgs
        except:
            print("get_comments_error")
            return "get_comments_error"

    # delete post by postID
    def deletePostByPostID(postID):
        try:
            GCP_DB.collection(u'Posts').document(postID).delete()
            # delete comments of that post if any
            comments = PostsDB.getCommentsByPostID(postID)
            if len(comments) != 0:
                for comment in comments:
                    GCP_DB.collection(u'Comments').document(
                        comment.commentID).delete()
            # delete likes of that post if any
            likes = PostsDB.getLikesByPostID(postID)
            if len(likes) != 0:
                for like in likes:
                    GCP_DB.collection(u'Likes').document(like.likeID).delete()
        except:
            print("delete_post_error")
            return "delete_post_error"

    # get new posts that is later than given dateTime

    def getNewPosts(dateTime):
        try:
            posts = []
            # convertedDateTime = datetime.strptime(dateTime, "%d/%m/%Y %H:%M:%S")
            posts_ref = GCP_DB.collection(u'Posts').where(
                u'dateTime', u'>', dateTime).get()

            for doc in posts_ref:
                docDict = doc.to_dict()
                post = Post(docDict['postID'], docDict['userID'], docDict['dateTime'],
                            docDict['mediaURL'], docDict['mediaType'], docDict['likesCount'], docDict['commentsCount'])
                posts.append(post)

            sortedPosts = sorted(posts, key=operator.attrgetter("dateTime"))

            return sortedPosts

        except:
            print("get_new_posts_error")
            return "get_new_posts_error"

    # get posts that is equal or less than given dateTime

    def getPrevPosts(dateTime):
        try:
            posts = []
            posts_ref = GCP_DB.collection(u'Posts').where(
                u'dateTime', u'<=', dateTime).get()

            for doc in posts_ref:
                docDict = doc.to_dict()
                post = Post(docDict['postID'], docDict['userID'], docDict['dateTime'],
                            docDict['mediaURL'], docDict['mediaType'], docDict['likesCount'], docDict['commentsCount'])
                posts.append(post)

            sortedPosts = sorted(posts, key=operator.attrgetter("dateTime"))

            return sortedPosts

        except:
            print("get_prev_posts_error")
            return "get_prev_posts_error"

    # transfer inapprpropriate post to censored collection and delete it from original post
    def censor(post: Post):
        # 'Censored', 'Posts', 'Users', 'Likes', 'Comments', 'Topics'
        try:
            GCP_DB.collection(u'Censored').document(
                post.postID).set(post.to_dict())
            PostsDB.justDelete(post)
        except:
            print("censor_post_error")
            return "censor_post_error"

    def justDelete(post):
        # 'Censored', 'Posts', 'Users', 'Likes', 'Comments', 'Topics'
        try:
            PostsDB.deletePostByPostID(post.postID)
            PostsDB.updatePostsCountByUserID(post.userID)
            PostsDB.updateLikesCountByUserID(post.userID)
            PostsDB.updateCommentsCountByUserID(post.userID)
        except:
            print("just_delete_error")
            return "just_delete_error"

    # get number of censored posts by userID

    def getWarningCount(userID):
        try:
            posts_ref = GCP_DB.collection(u'Censored')
            query_ref = posts_ref.where(u'userID', u'==', userID).get()
            no_of_posts = len(query_ref)
            return no_of_posts
        except:
            print("get_warning_count_error")
            return "get_warning_count_error"

    # get warning contents by user id

    def getWarnedContents(userID):
        try:
            warningPosts = []
            posts_ref = GCP_DB.collection(u'Censored')
            query_ref = posts_ref.where(u'userID', u'==', userID).get()

            for doc in query_ref:
                docDict = doc.to_dict()
                post = Post(docDict['postID'], docDict['userID'], docDict['dateTime'],
                            docDict['mediaURL'], docDict['mediaType'], docDict['likesCount'], docDict['commentsCount'])
                warningPosts.append(post)

            warningPosts.sort(key=operator.attrgetter(
                "dateTime"), reverse=True)

            return warningPosts
        except:
            print("get_warning_contents_error")
            return "get_warning_contents_error"

    # get list of censored users

    def getCensoredUsers():
        try:
            users = set()
            posts_ref = GCP_DB.collection(u'Censored').get()

            for doc in posts_ref:
                userID = doc.to_dict()['userID']
                users.add(userID)

            names = []
            for user in users:
                names.append(UsersDB.getName(user))

            return names

        except:
            print("get_censored_users_error")
            return "get_censored_users_error"
