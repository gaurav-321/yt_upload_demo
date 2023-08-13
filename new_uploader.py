#!/usr/bin/python

import os
import random
import sys
import time

import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner',
    "https://www.googleapis.com/auth/youtube.upload",
    'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'
]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=SCOPES,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
    credentials.refresh(httplib2.Http())
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


def initialize_upload(youtube, file, title, description, category, keywords, privacyStatus, thumbnail):
    tags = None
    if keywords:
        tags = keywords.split(",")

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category,
            'thumbnails': {
                'default': {
                    'url': thumbnail
                }
            }
        },
        'status': {
            'privacyStatus': privacyStatus
        }
    }

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )

    vid_id = resumable_upload(insert_request)
    return vid_id


# This method implements an exponential backoff strategy to resume a
# failed upload.
def add_endscreen(youtube, vid_id):
    end_screen = {
        "items": [
            {
                "type": "recommendedVideos"
            }
        ]
    }

    response = youtube.videos().update(
        part="status,endScreen",
        body={
            "id": "video_id",
            "endScreen": end_screen
        }
    ).execute()

    print(response)


def add_comment(youtube, vid_id, comment_text):
    request_body = {
        'snippet': {
            'videoId': vid_id,
            'topLevelComment': {
                'snippet': {
                    'textOriginal': comment_text
                }
            }
        }
    }
    response = youtube.commentThreads().insert(
        part='snippet',
        body=request_body
    ).execute()


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." % response['id'])
                    return response['id']
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


class Video():
    def __init__(self, file, title, thumbnail):
        self.file = file
        self.tile = title
        self.description = """Reddit Story time. Check out best stories on reddit in awesome voice.

🔔 Subscribe!
👍 Like this video if you want to see more videos!

#redditstories #redditmemes #maliciouscompliance 

If you don't want your story in this video please email me at redditvideos9910@gmail.com :) I will happily remove it


Credit: Author's names will be said before story, unless it's been sent to us and they've asked to include their 
name. Ignore below \n\n\n\n\n\n  """ + open("keywords.txt").read()
        keywords = open("keywords.txt").read().split(", ")
        random.shuffle(keywords)
        self.category = 24
        self.keywords = keywords[:30]
        self.privacyStatus = "public"
        self.vid_id = None
        self.thumbnail = thumbnail

    def upload(self, youtube):
        try:
            self.vid_id = initialize_upload(youtube,
                                            self.file,
                                            self.tile,
                                            self.description,
                                            self.category,
                                            self.keywords,
                                            self.privacyStatus,
                                            self.thumbnail)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            if "quota" in str(e):
                exit()


if __name__ == '__main__':
    file = r"your_video_file"
    title = "Your Title"
    desc = "demo desc"
    video_category = 24
    tags = "s,f,f"
    privacy = "public"
    video = Video(file, title, tags)
    youtube = get_authenticated_service()
    if video.vid_id:
        add_comment(youtube, video.vid_id, "hello")
