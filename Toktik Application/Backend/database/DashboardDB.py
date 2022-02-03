from Backend.classes import Post
from Backend.classes import User
from Backend.database import GCP_STORAGE
from Backend.initGCP import InitGCP
import operator
import threading
from datetime import datetime

# Initialize to GCP
GCP_DB = InitGCP.initDB()
GCP_STORAGE = InitGCP.initStorage()


class DashboardDB:
    participationsCount = 0
    postsCount = 0
    commentsCount = 0
    likesCount = 0
    mostLikedPost = ""
    latestPost = ""
    rankedUsers = []
    mostContributors = []

    # return number of users only with name
    def getParticipantsCount():
        try:
            users_ref = GCP_DB.collection(u'Users')
            query_ref = users_ref.where(u'name', u'!=', "").get()
            return len(query_ref)
        except:
            print("get_participants_error")
            return "get_participants_error"

    # return number of posts posted by participants
    def getPostsCount():
        try:
            posts_ref = GCP_DB.collection(u'Posts').get()
            return len(posts_ref)
        except:
            print("get_posts_count_error")
            return "get_posts_count_error"

    # return number of comments posted by participants
    def getCommentsCount():
        try:
            comments_ref = GCP_DB.collection(u'Comments').get()
            return len(comments_ref)
        except:
            print("get_comments_count_error")
            return "get_comments_count_error"

    # return number of likes across all posts by participants
    def getLikesCount():
        try:
            likes_ref = GCP_DB.collection(u'Likes').get()
            return len(likes_ref)
        except:
            print("get_likes_count_error")
            return "get_likes_count_error"

    # return 2 post in a list -> [0] is most Liked, [1] is most recent
    def getPostWithMostLikesAndRecent():
        try:
            # default date to compare datetime
            counts = [0, datetime.strptime(
                '03/12/2021 15:33:28', "%d/%m/%Y %H:%M:%S")]
            attributes = ['likesCount', 'dateTime']
            posts = ["", ""]
            posts_ref = GCP_DB.collection(u'Posts').get()
            for doc in posts_ref:
                docDict = doc.to_dict()
                post = Post(docDict['postID'], docDict['userID'], docDict['dateTime'],
                            docDict['mediaURL'], docDict['mediaType'], docDict['likesCount'], docDict['commentsCount'])
                for i in range(2):
                    if i == 0:
                        if docDict[attributes[i]] > counts[i]:
                            posts[i] = post
                            counts[i] = docDict[attributes[i]]
                    else:
                        postDate = datetime.strptime(
                            docDict[attributes[i]], "%d/%m/%Y %H:%M:%S")
                        if postDate > counts[i]:
                            posts[i] = post
                            counts[i] = datetime.strptime(
                                docDict[attributes[i]], "%d/%m/%Y %H:%M:%S")

            return posts
        except:
            print("get_post_most_like_recent_error")
            return "get_post_most_like_recent_error"

    def downloadFile(filePrefix, mediaURL):
        bucketName = "dscworkshopbucket"
        bucket = GCP_STORAGE.bucket(bucketName)
        front = "https://storage.cloud.google.com/dscworkshopbucket/"
        back = "?authuser=0"
        sourceFileName = mediaURL.replace(front, "").replace(back, "")
        blob = bucket.blob(sourceFileName)
        destFileName = filePrefix + sourceFileName.split(".")[-1]
        blob.download_to_filename(destFileName)
        return destFileName

    # Create an Event for notifying main thread.
    callback_done_users = threading.Event()
    callback_done_posts = threading.Event()
    callback_done_comments = threading.Event()
    callback_done_likes = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot_users(doc_snapshot, changes, read_time):
        try:
            DashboardDB.participationsCount = DashboardDB.getParticipantsCount()
            DashboardDB.rankedUsers = DashboardDB.sortRanking()
            DashboardDB.mostContributors = DashboardDB.getMostContributors()
            #print("Participants count: {}".format(DashboardDB.participationsCount))
            #print("Ranking: {}".format(DashboardDB.rankedUsers))
            DashboardDB.callback_done_users.set()
        except:
            print("snapshot_users_error")
            return "snapshot_users_error"

    def realTimeUpdatesUsers():
        try:
            doc_ref = GCP_DB.collection(u'Users')
            doc_ref.on_snapshot(DashboardDB.on_snapshot_users)
        except:
            print("realtime_users_error")
            return "realtime_users_error"

    # Create a callback on_snapshot function to capture changes

    def on_snapshot_posts(doc_snapshot, changes, read_time):
        try:
            DashboardDB.postsCount = DashboardDB.getPostsCount()
            DashboardDB.mostLikedPost = DashboardDB.getPostWithMostLikesAndRecent()[
                0]
            DashboardDB.latestPost = DashboardDB.getPostWithMostLikesAndRecent()[
                1]
            DashboardDB.rankedUsers = DashboardDB.sortRanking()
            # print("Post count: {}".format(DashboardDB.postsCount))
            # print("Most Liked Post: {}".format(DashboardDB.mostLikedPost.postID))
            # print("Latest Post: {}".format(DashboardDB.latestPost.postID))
            # print("Ranking: {}".format(DashboardDB.rankedUsers))
            # print("kings: {}".format(DashboardDB.kings))
            DashboardDB.callback_done_posts.set()
        except:
            print("snapshot_posts_error")
            return "snapshot_posts_error"

    # real time updates with firestore db
    def realTimeUpdatesPosts():
        try:
            doc_ref = GCP_DB.collection(u'Posts')
            doc_ref.on_snapshot(DashboardDB.on_snapshot_posts)
        except:
            print("realtime_posts_error")
            return "realtime_posts_error"

     # Create a callback on_snapshot function to capture changes
    def on_snapshot_comments(doc_snapshot, changes, read_time):
        try:
            DashboardDB.commentsCount = DashboardDB.getCommentsCount()
            # print("Comment Count: {}".format(DashboardDB.commentsCount))
            DashboardDB.callback_done_comments.set()
        except:
            print("snapshot_comments_error")
            return "snapshot_comments_error"

    # real time updates with firestore db
    def realTimeUpdatesComments():
        try:
            doc_ref = GCP_DB.collection(u'Comments')
            doc_ref.on_snapshot(DashboardDB.on_snapshot_comments)
        except:
            print("realtime_comments_error")
            return "realtime_comments_error"

    # Create a callback on_snapshot function to capture changes

    def on_snapshot_Likes(doc_snapshot, changes, read_time):
        try:
            DashboardDB.likesCount = DashboardDB.getLikesCount()
            # print("Likes Count: {}".format(DashboardDB.likesCount))
            DashboardDB.callback_done_likes.set()
        except:
            print("snapshot_likes_error")
            return "snapshot_likes_error"

    # real time updates with firestore db
    def realTimeUpdatesLikes():
        try:
            doc_ref = GCP_DB.collection(u'Likes')
            doc_ref.on_snapshot(DashboardDB.on_snapshot_Likes)
        except:
            print("realtime_likes_error")
            return "realtime_likes_error"

    # # get king of each topic based on likes count
    # def getKingOfEachTopics():
    #     try:
    #         posts = []
    #         posts_ref = GCP_DB.collection(u'Posts').get()
    #         for doc in posts_ref:
    #             docDict = doc.to_dict()
    #             post = Post(docDict['postID'], docDict['userID'], docDict['topicID'], docDict['dateTime'],
    #                 docDict['mediaURL'], docDict['mediaType'], docDict['likesCount'], docDict['commentsCount'], docDict['viewsCount'])
    #             posts.append(post)

    #         sortedPosts = sorted(posts, key=operator.attrgetter('likesCount'), reverse=True)

    #         topicCount = 5
    #         kings = []
    #         for i in range(topicCount):
    #             for post in sortedPosts:
    #                 if post.topicID == str(i+1) and post.likesCount > 0:
    #                     name = UsersDB.getName(post.userID)
    #                     kings.append(name)
    #                     break
    #             else:
    #                 kings.append("")
    #         #print(kings)
    #         return kings

    #     except:
    #         print("get_king_topics_error")
    #         return "get_king_topics_error"

    def getName(account):
        users_ref = GCP_DB.collection(u'Users')
        query_ref = users_ref.where(u'userID', u'==', account).get()
        return query_ref[0].to_dict()['name']

    # get user with most contributions in terms of likes, comments and posts
    def getMostContributors():
        try:
            counts = [0, 0, 0]
            attributes = ['likesCount', 'commentsCount', 'postsCount']
            users = ["", "", ""]
            ref = GCP_DB.collection(u'Users').get()
            for doc in ref:
                docDict = doc.to_dict()
                for i in range(3):
                    if docDict[attributes[i]] > counts[i]:
                        users[i] = docDict['name']
                        counts[i] = docDict[attributes[i]]
            mostLiked = DashboardDB.mostLikedPost
            users.insert(0, "")
            if mostLiked:
                name = DashboardDB.getName(mostLiked.userID)
                users[0] = name
            return users
        except:
            print("get_most_contributors_error")
            return "get_most_contributors_error"

    # sort by progress first, then number of achievements they have
    def sortRanking():
        try:
            # criteria: 5 posts and 10 likes/comments
            postCriteria = 5
            lcCriteria = 10
            # classify according to tiers
            bothSatisfied = []
            postSatisfied = []
            notSatisfied = []
            ref = GCP_DB.collection(u'Users').where(u'name', u'!=', "").get()
            for doc in ref:
                docDict = doc.to_dict()
                user = User(userID=docDict['userID'], name=docDict['name'], likesCount=docDict['likesCount'],
                            commentsCount=docDict['commentsCount'], postsCount=docDict['postsCount'])
                postCount = user.postsCount
                lcCount = docDict['likesCount'] + docDict['commentsCount']
                if postCount < postCriteria:
                    notSatisfied.append(user)
                elif lcCount < lcCriteria:
                    postSatisfied.append(user)
                else:
                    bothSatisfied.append(user)
            # sort according to each tier's logic
            notSatisfied.sort(key=operator.attrgetter(
                'postsCount'), reverse=True)
            postSatisfied.sort(key=lambda obj: obj.likesCount +
                               obj.commentsCount, reverse=True)
            rankedUsers = bothSatisfied + postSatisfied + notSatisfied
            return rankedUsers
        except:
            print("sort_ranking_err")
            return "sort_ranking_err"
