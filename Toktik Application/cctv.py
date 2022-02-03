#!/usr/bin/env python3
from Backend import Backend as backend
import streamlit as st
from PIL import Image
import os

# states
if 'latestTime' not in st.session_state:
    st.session_state.latestTime = "01/12/2021 00:00:00"  # put oldest date
if 'mediaList' not in st.session_state:
    st.session_state.mediaList = []
if 'post' not in st.session_state:
    st.session_state.post = None
if 'fileName' not in st.session_state:
    st.session_state.fileName = ""


# Widgets
st.title('CCTV for TokTik')
CENSOREDUSERS = st.empty()
REMAINING = st.empty()
NEXTBUTTON = st.empty()
MEDIA = st.empty()
POSTID = st.empty()
DATETIME = st.empty()
CENSORBUTTON = st.empty()
JUSTDELBUTTON = st.empty()

# functions


def displayCensoredUsers():
    censoredUsers = backend.getCensoredUsers()
    with CENSOREDUSERS.expander("Censored Users"):
        st.write(censoredUsers)


def saveMedia(mediaURL):
    filePrefix = "CCTV."
    return backend.downloadMedia(filePrefix, mediaURL)


def removeSavedMedia():
    fileName = st.session_state.fileName
    if fileName:
        os.remove(fileName)


def cacheMedia(fileName, post):
    st.session_state.post = post
    st.session_state.fileName = fileName


def clearCache():
    st.session_state.post = None
    st.session_state.fileName = ""


def hasCache():
    return bool(st.session_state.post)


def displayRemaining():
    remaining = len(st.session_state.mediaList)
    message = "{} more new posts incoming!".format(remaining)
    REMAINING.write(message)


def display():
    fileName = st.session_state.fileName
    post = st.session_state.post
    if post.mediaType.startswith("video"):
        MEDIA.video(open(fileName, 'rb').read())
    else:
        MEDIA.image(Image.open(fileName), width=300)
    POSTID.write("PostID: " + post.postID)
    DATETIME.write("DateTime: " + post.dateTime)


def emptyDisplay():
    MEDIA.empty()
    POSTID.empty()
    DATETIME.empty()
    CENSORBUTTON.empty()


def getNewPosts():
    latest = st.session_state.latestTime
    incomingPosts = backend.getNewPosts(latest)
    if incomingPosts:
        st.session_state.latestTime = incomingPosts[-1].dateTime
        st.session_state.mediaList += incomingPosts
        displayRemaining()
    return st.session_state.mediaList


# logic
displayCensoredUsers()
displayRemaining()
wantNext = NEXTBUTTON.button("Next")
if wantNext:
    removeSavedMedia()
    clearCache()
    mediaList = getNewPosts()
    if mediaList:
        post = mediaList.pop(0)
        fileName = saveMedia(post.mediaURL)
        cacheMedia(fileName, post)
if hasCache():
    display()
    wantCensor = CENSORBUTTON.button("!! Censor !!")
    wantDel = JUSTDELBUTTON.button("Just Delete...")
    if wantCensor:
        backend.censor(st.session_state.post)
        CENSORBUTTON.empty()
        JUSTDELBUTTON.empty()
        st.success("This post has been censored")
    if wantDel:
        backend.justDelete(st.session_state.post)
        CENSORBUTTON.empty()
        JUSTDELBUTTON.empty()
        st.success("This post has been deleted")
else:
    emptyDisplay()
    st.success("There are no more posts at the moment")
