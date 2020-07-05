import requests
import os

from pyrler.utilities.wrappers import template_request
from pyrler.utilities.params_helper import *


class _Parler:
    """
    Base class for Parler API endpoints.
    """

    def __init__(self):
        self.parler_url = "https://api.parler.com"
        self.mst_cookie = os.environ['MST_COOKIE']
        self.jst_cookie = os.environ['JST_COOKIE']


    def _base_request(self, method, route, **kwargs):
        """
        Base request class.
        :param method: http method
        :param route: tapi route
        :param kwargs:
        :return: requests.Reponse
        """
        url = self.parler_url + route
        cookies = {'mst': self.mst_cookie,
                   'jst': self.jst_cookie}
        response = requests.request(method=method, cookies=cookies, url=url, **kwargs)
        return response


class Comment(_Parler):
    """
    Comments
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/comment", request_params=[ID, STARTKEY])
    def get_comment(self, id=None, startkey=None, **kwargs):
        """
        Get a comment identified by its ID.
        :param id: Comment ID
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/comment/creator", request_params=[ID, STARTKEY])
    def get_user_comments(self, id=None, startkey=None, **kwargs):
        """
        Returns a users comment history.
        :param id: User ID
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


    @template_request(method="POST", route="/v1/comment")
    def create_comment(self, parent_id, comment, links=[], **kwargs):
        """
        Post a comment to a parent object identified by its ID.

        Comment post data:
            {"body":"Science Rules!","parent": parent_id,"links":["https://en.wikipedia.org/wiki/File:Bill_Nye_2017.jpg"]}
        :param parent_id:
        :param comment:
        :param links:
        :param kwargs:
        :return:
        """
        if isinstance(links, str):
            links = [links]
        data = {"body": comment, "parent": parent_id, "links": links}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/comment/delete", request_params=[ID])
    def delete_comment(self, id=None, **kwargs):
        """
        Delete a comment identified by its ID.
        :param id:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/comment/vote")
    def vote_comment(self, comment_id, upvote=True, **kwargs):
        """
        Up-vote a comment when upvote=True.
        Down-vote a comment when upvote=False.

        Comment vote data:
            {"comment_id": comment_id, "up": True}

        :param comment_id:
        :param upvote:
        :param kwargs:
        :return:
        """
        data = {"comment_id": comment_id, "up": upvote}
        return self._base_request(data=data, **kwargs)


class Discover(_Parler):
    """
    Discover
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/discover/hashtags", request_params=[STARTKEY])
    def discover_hashtags(self, startkey=None, **kwargs):
        """
        Returns a list of promoted hashtags.
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/discover/news", request_params=[STARTKEY])
    def discover_news(self, startkey=None, **kwargs):
        """
        Returns a list of promoted news.
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/discover/users", request_params=[STARTKEY])
    def discover_users(self, startkey=None, **kwargs):
        """
        Returns a list of promoted users.
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/discover/posts", request_params=[STARTKEY])
    def discover_posts(self, startkey=None, **kwargs):
        """
        Returns a list of promoted posts.
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


class Feed(_Parler):
    """
    Feed
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/feed", request_params=[STARTKEY, LIMIT])
    def get_feed(self, startkey=None, limit=None, **kwargs):
        """
        Returns Parleys from the user's feed.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


class Follow(_Parler):
    """
    Follow
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/follow/followers", request_params=[ID, STARTKEY, LIMIT])
    def get_followers(self, id=None, startkey=None, limit=None, **kwargs):
        """
        Returns a user's followers.
        :param id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/follow/following", request_params=[ID, STARTKEY, LIMIT])
    def get_following(self, id=None, startkey=None, limit=None, **kwargs):
        """
        Returns users following a user.
        :param id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/follow/followers/pending", request_params=[ID, STARTKEY, LIMIT])
    def get_pending_followers(self, id=None, startkey=None, limit=None, **kwargs):
        """
        Returns followers pending approval.
        :param id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/follow/following/subscribed", request_params=[ID, STARTKEY, LIMIT])
    def get_subscribed_following(self, id=None, startkey=None, limit=None, **kwargs):
        """
        Returns users a user is subscribed to.
        :param id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/follow", request_params=[USERNAME])
    def follow_user(self, username=None, **kwargs):
        """
        Follow a user.
        :param username: username
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/follow/delete", request_params=[USERNAME])
    def unfollow_user(self, username=None, **kwargs):
        """
        Unfollow a user.
        :param username: username
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/follow/followers/pending/approve", request_params=[USERNAME])
    def approve_follower(self, username=None, **kwargs):
        """
        Approve a pending follower.
        :param username:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/follow/followers/pending/deny", request_params=[USERNAME])
    def deny_follower(self, username=None, **kwargs):
        """
        Deny a pending follower.
        :param username:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/follow/following/subscribed", request_params=[ID])
    def subscribed(self, id=None, **kwargs):
        """
        Returns a list of a user's subscribed accounts.
        :param id:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


class Hashtag(_Parler):
    """
    Hashtag
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/hashtag", request_params=[SEARCH, STARTKEY, LIMIT])
    def search(self, search=None, startkey=None, limit=None, **kwargs):
        """
        Returns result of a hashtag search.
        :param search: hashtag
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


class Identity(_Parler):
    """
    Identity
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/identity/status", request_params=[])
    def get_user_verification_status(self, **kwargs):
        return self._base_request(**kwargs)


class Messaging(_Parler):
    """
    Messaging
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/messaging/conversations", request_params=[STARTKEY, LIMIT])
    def get_conversations(self, startkey=None, limit=None, **kwargs):
        """
        Returns the user's conversations.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/messaging/conversations/user", request_params=[SEARCH, STARTKEY, LIMIT])
    def search_messenger_users(self, search=None, startkey=None, limit=None, **kwargs):
        """
        Returns
        :param search: username
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/messaging/conversations/user/<id>", request_params=[SEARCH, STARTKEY, LIMIT])
    def get_user_conversations(self, id, startkey=None, limit=None, **kwargs):
        """
        Returns conversations with a user.
        :param id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/messaging/conversations/<id>/messages", request_params=[SEARCH, STARTKEY, LIMIT])
    def get_conversation(self, id, startkey=None, limit=None, **kwargs):
        """
        Returns a conversation.
        :param id: Conversation ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/messaging/conversations/requests", request_params=[STARTKEY, LIMIT])
    def get_conversations_requests(self, search=None, startkey=None, limit=None, **kwargs):
        """
        Returns conversation requests.
        :param search: username
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/messaging/counts", request_params=[STARTKEY, LIMIT])
    def get_conversations_count(self, startkey=None, limit=None, **kwargs):
        """
        Returns conversation request and unread conversation count.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/messaging/conversations/{id}/accept", request_params=[ID])
    def accept_conversation_request(self, id=None, **kwargs):
        """
        Accept conversation request.
        :param id: Conversation ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/messaging/conversations/{id}/deny", request_params=[ID])
    def deny_conversation_request(self, id=None, **kwargs):
        """
        Deny conversation request.
        :param id: Conversation ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/messaging/conversations/{id}/mute", request_params=[ID])
    def mute_conversation_request(self, id=None, **kwargs):
        """
        Mute conversation request.
        :param id: Conversation ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/messaging/conversations/{id}/spam", request_params=[ID])
    def spam_conversation_request(self, id=None, **kwargs):
        """
        Report conversation request as spam.
        :param id: Conversation ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


class Moderation(_Parler):
    """
    Moderation
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/moderation/approved", request_params=[ORGANIZATION, STARTKEY, LIMIT, REVERSE])
    def get_approved_comments(self, organization=None, startkey=None, limit=None, reverse=True, **kwargs):
        """
        Returns approved comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/moderation/denied", request_params=[ORGANIZATION, STARTKEY, LIMIT, REVERSE])
    def get_deleted_comments(self, organization=None, startkey=None, limit=None, reverse=True, **kwargs):
        """
        Returns deleted comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/moderation/filter/word", request_params=[ORGANIZATION, STARTKEY, LIMIT, REVERSE, ACTION])
    def get_filtered_words(self, organization=None, startkey=None, limit=None, action=None, reverse=True, **kwargs):
        """
        Returns filtered words.
        :param organization:
        :param startkey:
        :param limit:
        :param action:
        :param reverse:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/moderation/muted", request_params=[ORGANIZATION, STARTKEY, LIMIT, REVERSE, ACTION])
    def get_muted_comments(self, organization=None, startkey=None, limit=None, reverse=True, **kwargs):
        """
        Returns muted comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/moderation/pending", request_params=[ORGANIZATION, STARTKEY, LIMIT, REVERSE, ACTION])
    def get_pending_comments(self, organization=None, startkey=None, limit=None, reverse=True, **kwargs):
        """
        Returns pending comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/moderation/spam", request_params=[ORGANIZATION, STARTKEY, LIMIT, REVERSE, ACTION])
    def get_spam_comments(self, organization=None, startkey=None, limit=None, reverse=True, **kwargs):
        """
        Returns comments flagged as spam.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/moderation/accept")
    def approve_comment(self, comment_id, **kwargs):
        """
        Approve a comment.
        :param comment_id:
        :param kwargs:
        :return:
        """
        data = {"comments": [comment_id]}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/moderation/deny")
    def deny_comment(self, comment_id, **kwargs):
        """
        Deny a comment.
        :param comment_id:
        :param kwargs:
        :return:
        """
        data = {"comments": [comment_id]}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/moderation/mute")
    def mute_comment(self, comment_id, **kwargs):
        """
        Mute a comment.
        :param comment_id:
        :param kwargs:
        :return:
        """
        data = {"comments": [comment_id]}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/moderation/spam")
    def spam_comment(self, comment_id, **kwargs):
        """
        Mark comment as spam.
        :param comment_id:
        :param kwargs:
        :return:
        """
        data = {"comments": [comment_id]}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="v1/moderation/filter/word")
    def filter_word(self, word, action, **kwargs):
        """
        Perform actions on filtered words.
        Allowed actions:
            default :
            approve :
            banUser :
            banUserNotification :
            deny :
            denyDetailed :
            muteComment :
            muteUser :
            review :
            temporaryBan :
        :param word: word to filter
        :param action: type of filter action to apply
        :param kwargs:
        :return:
        """
        data = {"words":[word],"action":action}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="v1/moderation/filter/word/delete")
    def delete_filter_word(self, word, **kwargs):
        """
        Deletes filtered word.
        :param word: word to filter
        :param kwargs:
        :return:
        """
        data = {"words":[word]}
        return self._base_request(data=data, **kwargs)


class News(_Parler):
    """
    News
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/news", request_params=[STARTKEY, LIMIT])
    def get_news(self, startkey=None, limit=None, **kwargs):
        """
        Returns news feed.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/news/search", request_params=[SEARCH, STARTKEY, LIMIT])
    def search_news(self, search=None, startkey=None, limit=None, **kwargs):
        """
        Search news feed.
        :param search:
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


class Notification(_Parler):
    """
    Notification
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/notification", request_params=[STARTKEY, LIMIT])
    def get_notifications(self, startkey=None, limit=None, **kwargs):
        """
        Returns notifications.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/notification/count", request_params=[])
    def get_notification_count(self, **kwargs):
        """
        Returns notification count.
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="v1/notification")
    def update_notification(self, id, **kwargs):
        """
        Updates a notification status.
        :param id: Notification ID
        :param kwargs:
        :return:
        """
        data = {"id":[id]}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="v1/notification/delete", request_params=[ID])
    def delete_notification(self, id=None, **kwargs):
        """
        Deletes a notification.
        :param id: Notification ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="v1/notification/all/delete")
    def delete_all_notifications(self, **kwargs):
        """
        Deletes all notifications.
        :param kwargs:
        :return:
        """
        data = {"id":""}
        return self._base_request(data=data, **kwargs)


class Photo(_Parler):
    """
    Photo
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/photo", request_params=[ID])
    def get_photo(self, id=None, **kwargs):
        """
        Returns a photo.
        :param id:  Photo ID.
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


class Post(_Parler):
    """
    Post
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/post", request_params=[ID])
    def get_post(self, id=None, **kwargs):
        """
        Returns a post.
        :param id: post ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/comment", request_params=[ID, REVERSE])
    def get_post_comments(self, id=None, reverse=True, **kwargs):
        """
        Returns a post's comments.
        :param id: post ID
        :param reverse:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/post/<id>/impressions")
    def get_impressions(self, id, **kwargs):
        """
        Returns the impressions on a post.
        This method requires ownership of the target post.
        :param id: post ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/post/creator", request_params=[ID, STARTKEY])
    def get_user_posts(self, id=None, startkey=None, **kwargs):
        """
        Returns posts created by a user.
        :param id: User ID
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/post/creator/liked", request_params=[ID, STARTKEY])
    def get_liked_posts(self, id=None, startkey=None, **kwargs):
        """
        Returns posts liked by a user.
        :param id: post ID
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/post/creator/media", request_params=[ID, STARTKEY])
    def get_creator_media(self, id=None, startkey=None, **kwargs):
        """
        Returns media posted by a user.
        :param id: User ID
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/post/hashtag", request_params=[TAG, STARTKEY])
    def search_by_hashtag(self, tag=None, startkey=None, **kwargs):
        """
        Returns a list of posts.
        :param tag: hashtag
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/post")
    def post(self, post, links=[], **kwargs):
        """
        Post a Parley.
        Data:
            {"body":"hello world🍆","parent":null,"links":[],"state":4}
        :param post:
        :param kwargs:
        :return:
        """
        if isinstance(links, str):
            links = [links]
        data = {"body":post, "parent": None,"links":links,"state": 4}
        return self._base_request(data=data, **kwargs)

    @template_request(method="GET", route="/v1/post/delete", request_params=[ID])
    def delete_post(self, id=None, **kwargs):
        """
        Delete a post.
        :param id: Post ID
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="POST", route="/v1/post/upvote")
    def upvote(self, id, **kwargs):
        """
        Updoot a post.
        :param id:
        :param kwargs:
        :return:
        """
        data = {"id": id}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/post/upvote/delete")
    def rescind_upvote(self, id, **kwargs):
        """
        I'm officially rescinding my updoot.
        :param id: Post ID
        :param kwargs:
        :return:
        """
        data = {"id": id}
        return self._base_request(data=data, **kwargs)


class Profile(_Parler):
    """
    Profile
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/profile", request_params=[ID, USERNAME])
    def get_user_profile(self, id=None, username=None, **kwargs):
        """
        Returns a user profile.
        :param id: User ID
        :param username:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/profile", request_params=[])
    def get_profile_settings(self, **kwargs):
        """
        Returns current user profile setting.
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="PATCH", route="/v1/profile", request_params=[])
    def update_profile(self, **kwargs):
        """
        Updates the profile of the logged in user.

        Implement me!
        :param kwargs:
        :return:
        """
        pass

    @template_request(method="PATCH", route="/v1/profile/settings", request_params=[])
    def update_profile_settings(self, **kwargs):
        """
        Updates the profile setting of the logged in user.

        Implement me!
        :param kwargs:
        :return:
        """
        pass

    @template_request(method="POST", route="/v1/profile/badge/display")
    def change_badge(self, **kwargs):
        """
        Implement me!
        :param kwargs:
        :return:
        """
        return ""

    @template_request(method="POST", route="/v1/profile/cover-photo")
    def upload_cover_photo(self, file_name, **kwargs):
        """
        Upload profile cover photo.
        :param file_name: path to file
        :param kwargs:
        :return:
        """
        headers = {'Content-Disposition': 'form-data',
                   'Content-Type': 'image/jpeg',
                   'name': 'upload',
                   'filename': 'cover-photo.jpeg'}
        with open(file_name, 'rb') as f:
            data = f
        return self._base_request(headers=headers, data=data, **kwargs)

    @template_request(method="POST", route="/v1/profile/photo")
    def upload_profile_photo(self, file_name, **kwargs):
        """
        Upload profile photo.
        :param file_name: path to file
        :param kwargs:
        :return:
        """
        headers = {'Content-Disposition': 'form-data',
                   'Content-Type': 'image/jpeg',
                   'name': 'upload',
                   'filename': 'photo.jpeg'}
        with open(file_name, 'rb') as f:
            data = f
        return self._base_request(headers=headers, data=data, **kwargs)


class User(_Parler):
    """
    User
    """

    def __init__(self):
        _Parler.__init__(self)

    @template_request(method="GET", route="/v1/user/block", request_params=[STARTKEY])
    def get_blocked_users(self, startkey=None, **kwargs):
        """
        Returns a list of blocked users.
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/user/exists", request_params=[USERNAME])
    def get_users_exists(self, username=None, **kwargs):
        """
        Returns user exists status.
        :param username:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/user/mute", request_params=[STARTKEY])
    def get_muted_users(self, startkey=None, **kwargs):
        """
        Returns a list of muted users.
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/users", request_params=[SEARCH, STARTKEY])
    def search_users(self, search=None, startkey=None, **kwargs):
        """
        Search for a user by their account name.
        :param search:
        :param startkey:
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)

    @template_request(method="GET", route="/v1/users/rss", request_params=[])
    def get_suggested_users(self, **kwargs):
        """
        Returns a list of suggested followers.
        :param kwargs:
        :return:
        """
        return self._base_request(**kwargs)


    @template_request(method="POST", route="/v1/user/block")
    def block_user(self, username, **kwargs):
        """
        Block a user.
        :param username:
        :param kwargs:
        :return:
        """
        data = {"username": username}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/user/block/delete")
    def unblock_user(self, id, **kwargs):
        """
        Unblock a user.
        :param id:
        :param kwargs:
        :return:
        """
        data = {"id": id}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/user/dislike")
    def dislike_user(self, id, **kwargs):
        """
        Dislike a user.
        :param id:
        :param kwargs:
        :return:
        """
        data = {"id": id}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/user/mute")
    def mute_user(self, username, **kwargs):
        """
        Mute a user.
        :param username:
        :param kwargs:
        :return:
        """
        data = {"username": username}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/user/mute/delete")
    def unmute_user(self, id, **kwargs):
        """
        Unmute a user.
        :param id:
        :param kwargs:
        :return:
        """
        data = {"id": id}
        return self._base_request(data=data, **kwargs)

    @template_request(method="POST", route="/v1/user/report")
    def report(self, id, reason, message="", **kwargs):
        """
        Report a user.

        Data:
            {reason: "spam", message: "wow much spam", id: id}

        :param id:
        :param reason:
        :param message:
        :param kwargs:
        :return:
        """
        reasons = ["spam", "terror", "ads", "slander", "blackmail", "threats", "crime",
                   "porn", "nude", "obscenity", "plagiarism", "bribe", "killing", "illegal"]
        data = {reason: reason, message: message, id: id}
        return self._base_request(data=data, **kwargs)
