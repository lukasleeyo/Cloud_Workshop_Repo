from Backend.initGCP import InitGCP
# Initialize to GCP
GCP_DB = InitGCP.initDB()


class ContributionsDB:
    # check how many posts this user has posted
    def checkPostCount(userID):
        try:
            # Create a reference to the Posts collection
            posts_ref = GCP_DB.collection(u'Posts')
            # Create a query against the collection
            query_ref = posts_ref.where(u'userID', u'==', userID).get()
            no_of_posts = len(query_ref)
            return no_of_posts
        except:
            print("check_post_count_error")
            return "check_post_count_error"

    # check how many likes and comments this user has made
    def checkReplyCount(userID):
        try:
            # Create a reference to the Likes and Comments collection
            likes_ref = GCP_DB.collection(u'Likes')
            comments_ref = GCP_DB.collection(u'Comments')
            # Create a query against the Likes and Comments collection
            likesQuery_ref = likes_ref.where(u'userID', u'==', userID).get()
            commentsQuery_ref = comments_ref.where(
                u'userID', u'==', userID).get()

            noOfReplies = len(likesQuery_ref) + len(commentsQuery_ref)
            return noOfReplies
        except:
            print("check_reply_count_error")
            return "check_reply_count_error"

     # check how many likes this user has made

    def checkLikesCount(userID):
        try:
            likes_ref = GCP_DB.collection(u'Likes')
            likesQuery_ref = likes_ref.where(u'userID', u'==', userID).get()

            noOfReplies = len(likesQuery_ref)
            return noOfReplies
        except:
            print("check_likes_count_error")
            return "check_likes_count_error"

    # check how many comments this user has made
    def checkCommentsCount(userID):
        try:
            comments_ref = GCP_DB.collection(u'Comments')
            commentsQuery_ref = comments_ref.where(
                u'userID', u'==', userID).get()

            noOfReplies = len(commentsQuery_ref)
            return noOfReplies
        except:
            print("check_reply_count_error")
            return "check_reply_count_error"
