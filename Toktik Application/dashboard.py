#!/usr/bin/env python3
from Backend.database import DashboardDB as DB
import streamlit as st
from PIL import Image
import time
from datetime import timedelta as timer

# Constants
imageFormats = ["png", "jpg", "jpeg"]
videoFormats = ["mp4", "avi"]
legend = """💕 You have a post that is most liked!
📸 You made the most number of posts!
😘 You liked most number of posts!
💬 You commented most number of times!"""

# Widgets
INSTRUCTION = st.container()
with INSTRUCTION:
    STARTBUTTON = st.empty()

TIMER = st.empty()
INFOPAGE1 = st.container()

with INFOPAGE1:
    C1, C2 = st.columns([1, 1])
    C3, C4 = st.columns([1, 1])
    SPACE = st.empty()
    MOSTLIKED, MOSTRECENT = st.columns([1, 1])

with C1:
    PARTICIPANTS = st.empty()
with C2:
    POSTS = st.empty()
with C3:
    LIKES = st.empty()
with C4:
    COMMENTS = st.empty()

with MOSTLIKED:
    LHEADER = st.empty()
    LINFO = st.empty()
    LMEDIA = st.empty()

with MOSTRECENT:
    RHEADER = st.empty()
    RINFO = st.empty()
    RMEDIA = st.empty()

INFOPAGE2 = st.container()
with INFOPAGE2:
    LEGEND = st.empty()
    PROGRESS = st.empty()


# Functions
@st.cache
def subscribeRealTimeUpdates():
    # call these 4 methods at initial stage only
    DB.realTimeUpdatesUsers()
    DB.realTimeUpdatesPosts()
    DB.realTimeUpdatesComments()
    DB.realTimeUpdatesLikes()


def displayTimer():
    TIMER.header("Time Left: " + str(timer(seconds=duration)))


def isShowingPage1():
    return int(duration/10) % 2 != 0


def wantShowMedia():
    return duration % 10 == 9


def erasePage1():
    PARTICIPANTS.empty()
    POSTS.empty()
    LIKES.empty()
    COMMENTS.empty()
    LHEADER.empty()
    LMEDIA.empty()
    LINFO.empty()
    SPACE.empty()
    RHEADER.empty()
    RMEDIA.empty()
    RINFO.empty()


def updateInfo1():
    PARTICIPANTS.subheader("Participants: {}".format(DB.participationsCount))
    POSTS.subheader("Posts: {}".format(DB.postsCount))
    LIKES.subheader("Likes: {}".format(DB.likesCount))
    COMMENTS.subheader("Comments: {}".format(DB.commentsCount))
    SPACE.subheader("")


def saveMedia(prefix, mediaURL):
    return DB.downloadFile(prefix, mediaURL)


def displayMedia(WIDGET, filename):
    ext = filename.split(".")[-1]
    if ext in videoFormats:
        WIDGET.video(open(filename, 'rb').read())
    else:
        WIDGET.image(Image.open(filename))


def updateMostLiked():
    LHEADER.subheader("💖 Most Liked Post")
    displayMedia(LMEDIA, mostLiked[1])
    with LINFO.container():
        st.markdown("**By " + DB.getName(mostLiked[0].userID) + "**")
        st.text(str(mostLiked[0].likesCount) + " likes")


def updateMostRecent():
    RHEADER.subheader("⏰ Most Recent Post")
    displayMedia(RMEDIA, mostRecent[1])
    with RINFO.container():
        st.markdown("**By " + DB.getName(mostRecent[0].userID) + "**")
        st.text("at " + mostRecent[0].dateTime)


def erasePage2():
    LEGEND.empty()
    PROGRESS.empty()


def updateInfo3():
    LEGEND.text(legend)
    achievements = ["💕", "😘", "💬", "📸"]
    achievers = DB.mostContributors
    rankedUsers = DB.rankedUsers
    with PROGRESS.container():
        NAME, POSTC, LC, ACH = st.columns([0.5, 1, 1, 0.3])
        NAME.markdown("**Name**")
        POSTC.markdown("**Posts**")
        LC.markdown("**Likes and Comments**")
        ACH.markdown("**Achievements**")
        for user in rankedUsers:
            postc = 1.0 if user.postsCount >= 3 else user.postsCount/3
            likesComments = user.likesCount + user.commentsCount
            lc = 1.0 if likesComments >= 10 else likesComments/10
            achieve = "  "
            for i in range(len(achievements)):
                if achievers[i] == user.name:
                    achieve += achievements[i] + " "
            addRow(user.name, postc, lc, achieve)


def addRow(name, postc, lc, ach):
    NAME, POSTC, LC, ACH = st.columns([0.5, 1, 1, 0.3])
    NAME.write(name)
    POSTC.progress(postc)
    LC.progress(lc)
    ACH.text(ach)


# Logic
subscribeRealTimeUpdates()

duration = TIMER.number_input("How many minutes?", 0, 20, 0) * 60
mostLiked = ["", ""]
mostRecent = ["", ""]  # post object, filename
if STARTBUTTON.button('Start', key='start'):
    if STARTBUTTON.button('Stop'):
        pass
    while duration > 0:
        duration -= 1
        displayTimer()
        if isShowingPage1():
            erasePage2()
            updateInfo1()
            if DB.mostLikedPost and wantShowMedia():
                if DB.mostLikedPost != mostLiked:
                    mostLiked[0] = DB.mostLikedPost
                    mostLiked[1] = saveMedia(
                        "mostLiked.", mostLiked[0].mediaURL)
                updateMostLiked()
            if DB.latestPost and wantShowMedia():
                if DB.mostLikedPost != mostLiked:
                    mostRecent[0] = DB.latestPost
                    mostRecent[1] = saveMedia(
                        "mostRecent.", mostRecent[0].mediaURL)
                updateMostRecent()
        else:
            erasePage1()
            updateInfo3()
        time.sleep(1)
