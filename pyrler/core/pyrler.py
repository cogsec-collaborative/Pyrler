import os
import sys
import requests
import logging
from pyrler.utilities.wrappers import paginate
from pyrler.utilities.logger import logger


class _Parler:
    """
    Base class for Parler API endpoints.
    """

    def __init__(self, log_stdout=True, log_file=None):
        self.parler_url = "https://api.parler.com"
        self.log_stdout = log_stdout
        self.log_file = log_file
        self.mst_cookie = os.environ['MST_COOKIE']
        self.jst_cookie = os.environ['JST_COOKIE']
        self.cookies = {'mst': self.mst_cookie, 'jst': self.jst_cookie}

        self.logger = self._logger()
        self.session = self._session()

    def _logger(self):
        if self.log_stdout:
            stdout_handler = logging.StreamHandler(sys.stdout)
            # stdout_handler.setLevel(logging.INFO)
            logger.addHandler(stdout_handler)

        if self.log_file:
            file_handler = logging.FileHandler(filename=self.log_file, mode='a+')
            # file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)
        return logger

    def _session(self):
        session = requests.Session()
        return session

    def _get_request(self, route, **kwargs):
        """
        GET request class.
        :param method: http method
        :param route: tapi route
        :param kwargs:
        :return: requests.Reponse
        """
        url = self.parler_url + route
        response = self.session.get(cookies=self.cookies, url=url, **kwargs)
        print(response.headers)
        logger.info(response.json())
        return response

    def _post_request(self, route, **kwargs):
        """
        POST request class.
        :param method: http method
        :param route: tapi route
        :param kwargs:
        :return: requests.Reponse
        """
        url = self.parler_url + route
        response = self.session.post(cookies=self.cookies, url=url, **kwargs)
        return response

    def _patch_request(self, route, **kwargs):
        """
        PATCH request class.
        :param method: http method
        :param route: tapi route
        :param kwargs:
        :return: requests.Reponse
        """
        url = self.parler_url + route
        response = self.session.patch(cookies=self.cookies, url=url, **kwargs)
        return response


class Comment(_Parler):
    """
    Comments
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    def get_comment(self, comment_id=None, startkey=None, **kwargs):
        """
        Get a comment identified by its ID.
        :param comment_id: Comment ID
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/comment"
        request_params = {"id": comment_id, "startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_user_comments(self, user_id=None, startkey=None, follow=False, **kwargs):
        """
        Returns a users comment history.
        :param user_id: User ID
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/comment/creator"
        request_params = {"id": user_id, "startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

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
        route = "/v1/comment"
        data = {"body": comment, "parent": parent_id, "links": links}
        return self._post_request(route=route, data=data, **kwargs)

    def delete_comment(self, comment_id=None, **kwargs):
        """
        Delete a comment identified by its ID.
        :param comment_id:
        :param kwargs:
        :return:
        """
        route = "/v1/comment/delete"
        request_params = {"id": comment_id}
        return self._post_request(route=route, params=request_params, **kwargs)

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
        route = "/v1/comment/vote"
        data = {"comment_id": comment_id, "up": upvote}
        return self._post_request(route=route, data=data, **kwargs)


class Discover(_Parler):
    """
    Discover
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def discover_hashtags(self, startkey=None, follow=False, **kwargs):
        """
        Returns a list of promoted hashtags.
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/discover/hashtags"
        request_params = {"startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def discover_news(self, startkey=None, follow=False, **kwargs):
        """
        Returns a list of promoted news.
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/discover/news"
        request_params = {"startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def discover_users(self, startkey=None, follow=False, **kwargs):
        """
        Returns a list of promoted users.
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/discover/users"
        request_params = {"startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def discover_posts(self, startkey=None, follow=False, **kwargs):
        """
        Returns a list of promoted posts.
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/discover/posts"
        request_params = {"startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)


class Feed(_Parler):
    """
    Feed
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def get_feed(self, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns Parleys from the user's feed.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/feed"
        request_params = {"startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)


class Follow(_Parler):
    """
    Follow
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def get_followers(self, user_id=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns a user's followers.
        :param user_id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/follow/followers"
        request_params = {"id": user_id, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_following(self, user_id=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns users following a user.
        :param user_id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/follow/following"
        request_params = {"id": user_id, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_pending_followers(self, user_id=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns followers pending approval.
        :param user_id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/follow/followers/pending"
        request_params = {"id": user_id, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_subscribed_following(self, user_id=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns users a user is subscribed to.
        :param user_id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/follow/following/subscribed"
        request_params = {"id": user_id, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    def follow_user(self, username=None, **kwargs):
        """
        Follow a user.
        :param username: username
        :param kwargs:
        :return:
        """
        route = "/v1/follow"
        request_params = {"username": username}
        return self._post_request(route=route, params=request_params, **kwargs)

    def unfollow_user(self, username=None, **kwargs):
        """
        Unfollow a user.
        :param username: username
        :param kwargs:
        :return:
        """
        route = "/v1/follow/delete"
        request_params = {"username": username}
        return self._post_request(route=route, params=request_params, **kwargs)

    def approve_follower(self, username=None, **kwargs):
        """
        Approve a pending follower.
        :param username:
        :param kwargs:
        :return:
        """
        route = "/v1/follow/followers/pending/approve"
        request_params = {"username": username}
        return self._post_request(route=route, params=request_params, **kwargs)

    def deny_follower(self, username=None, **kwargs):
        """
        Deny a pending follower.
        :param username:
        :param kwargs:
        :return:
        """
        route = "/v1/follow/followers/pending/deny"
        request_params = {"username": username}
        return self._post_request(route=route, params=request_params, **kwargs)

    def subscribed(self, user_id=None, **kwargs):
        """
        Returns a list of a user's subscribed accounts.
        :param user_id:
        :param kwargs:
        :return:
        """
        route = "/v1/follow/following/subscribed"
        request_params = {"id": user_id}
        return self._post_request(route=route, params=request_params, **kwargs)


class Hashtag(_Parler):
    """
    Hashtag
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def search(self, search=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns result of a hashtag search.
        :param search: hashtag
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/hashtag"
        request_params = {"search": search, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)


class Identity(_Parler):
    """
    Identity
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    def get_user_verification_status(self, **kwargs):
        route = "/v1/identity/status"
        return self._get_request(route=route, **kwargs)


class Messaging(_Parler):
    """
    Messaging
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def get_conversations(self, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns the user's conversations.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/messaging/conversations"
        request_params = {"startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def search_messenger_users(self, search=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns
        :param search: username
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/messaging/conversations/user"
        request_params = {"search": search, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_user_conversations(self, user_id, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns conversations with a user.
        :param id: User ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = f"/v1/messaging/conversations/user/{user_id}"
        request_params = {"id": user_id, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_conversation(self, conversation_id, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns a conversation.
        :param conversation_id: Conversation ID
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = f"/v1/messaging/conversations/{conversation_id}/messages"
        request_params = {"id": conversation_id, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_conversations_requests(self, search=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns conversation requests.
        :param search: username
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/messaging/conversations/requests"
        request_params = {"search": search, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_conversations_count(self, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns conversation request and unread conversation count.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/messaging/counts"
        request_params = {"startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def accept_conversation_request(self, conversation_id=None, follow=False, **kwargs):
        """
        Accept conversation request.
        :param conversation_id: Conversation ID
        :param kwargs:
        :return:
        """
        route = f"/v1/messaging/conversations/{conversation_id}/accept"
        request_params = {"id": conversation_id}
        return self._post_request(route=route, params=request_params, **kwargs)

    @paginate
    def deny_conversation_request(self, conversation_id=None, follow=False, **kwargs):
        """
        Deny conversation request.
        :param conversation_id: Conversation ID
        :param kwargs:
        :return:
        """
        route = f"/v1/messaging/conversations/{conversation_id}/deny"
        request_params = {"id": conversation_id}
        return self._post_request(route=route, params=request_params, **kwargs)

    @paginate
    def mute_conversation_request(self, conversation_id=None, follow=False, **kwargs):
        """
        Mute conversation request.
        :param conversation_id: Conversation ID
        :param kwargs:
        :return:
        """
        route = f"/v1/messaging/conversations/{conversation_id}/mute"
        request_params = {"id": conversation_id}
        return self._post_request(route=route, params=request_params, **kwargs)

    @paginate
    def spam_conversation_request(self, conversation_id=None, follow=False, **kwargs):
        """
        Report conversation request as spam.
        :param conversation_id: Conversation ID
        :param kwargs:
        :return:
        """
        route = "/v1/messaging/conversations/{id}/spam"
        request_params = {"id": conversation_id}
        return self._post_request(route=route, params=request_params, **kwargs)


class Moderation(_Parler):
    """
    Moderation
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def get_approved_comments(self, organization=None, startkey=None, limit=None, reverse=True, follow=False, **kwargs):
        """
        Returns approved comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/approved"
        request_params = {"organization": organization, "startkey": startkey, "limit": limit, "reverse": reverse}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_deleted_comments(self, organization=None, startkey=None, limit=None, reverse=True, follow=False, **kwargs):
        """
        Returns deleted comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/denied"
        request_params = {"organization": organization, "startkey": startkey, "limit": limit, "reverse": reverse}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_filtered_words(self, organization=None, startkey=None, limit=None, action=None, reverse=True, follow=False, **kwargs):
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
        route = "/v1/moderation/filter/word"
        request_params = {"organization": organization, "startkey": startkey, "limit": limit, "action":
            action, "reverse": reverse}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_muted_comments(self, organization=None, startkey=None, limit=None, reverse=True, follow=False, **kwargs):
        """
        Returns muted comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/muted"
        request_params = {"organization": organization, "startkey": startkey, "limit": limit, "reverse": reverse}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_pending_comments(self, organization=None, startkey=None, limit=None, reverse=True, follow=False, **kwargs):
        """
        Returns pending comments.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        route="/v1/moderation/pending"
        request_params = {"organization": organization, "startkey": startkey, "limit": limit, "reverse": reverse}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_spam_comments(self, organization=None, startkey=None, limit=None, reverse=True, follow=False, **kwargs):
        """
        Returns comments flagged as spam.
        :param organization:
        :param startkey:
        :param limit:
        :param reverse:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/spam"
        request_params = {"organization": organization, "startkey": startkey, "limit": limit, "reverse": reverse}
        return self._get_request(route=route, params=request_params, **kwargs)

    def approve_comment(self, comment_id, **kwargs):
        """
        Approve a comment.
        :param comment_id:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/accept"
        data = {"comments": [comment_id]}
        return self._post_request(route=route, data=data, **kwargs)

    def deny_comment(self, comment_id, **kwargs):
        """
        Deny a comment.
        :param comment_id:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/deny"
        data = {"comments": [comment_id]}
        return self._post_request(route=route, data=data, **kwargs)

    def mute_comment(self, comment_id, **kwargs):
        """
        Mute a comment.
        :param comment_id:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/mute"
        data = {"comments": [comment_id]}
        return self._post_request(route=route, data=data, **kwargs)

    def spam_comment(self, comment_id, **kwargs):
        """
        Mark comment as spam.
        :param comment_id:
        :param kwargs:
        :return:
        """
        route = "/v1/moderation/spam"
        data = {"comments": [comment_id]}
        return self._post_request(route=route, data=data, **kwargs)

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
        route = "v1/moderation/filter/word"
        data = {"words": [word], "action": action}
        return self._post_request(route=route, data=data, **kwargs)

    def delete_filter_word(self, word, **kwargs):
        """
        Deletes filtered word.
        :param word: word to filter
        :param kwargs:
        :return:
        """
        route = "v1/moderation/filter/word/delete"
        data = {"words": [word]}
        return self._post_request(route=route, data=data, **kwargs)


class News(_Parler):
    """
    News
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def get_news(self, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns news feed.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/news"
        request_params = {"startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def search_news(self, search=None, startkey=None, limit=None, follow=False, **kwargs):
        """
        Search news feed.
        :param search:
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/news/search"
        request_params = {"search": search, "startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)


class Notification(_Parler):
    """
    Notification
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def get_notifications(self, startkey=None, limit=None, follow=False, **kwargs):
        """
        Returns notifications.
        :param startkey:
        :param limit:
        :param kwargs:
        :return:
        """
        route = "/v1/notification"
        request_params = {"startkey": startkey, "limit": limit}
        return self._get_request(route=route, params=request_params, **kwargs)

    def get_notification_count(self, **kwargs):
        """
        Returns notification count.
        :param kwargs:
        :return:
        """
        route = "/v1/notification/count"
        return self._get_request(route=route, **kwargs)

    def update_notification(self, notification_id, **kwargs):
        """
        Updates a notification status.
        :param notification_id: Notification ID
        :param kwargs:
        :return:
        """
        route = "v1/notification"
        data = {"id": [notification_id]}
        return self._post_request(route=route, data=data, **kwargs)

    def delete_notification(self, notification_id=None, **kwargs):
        """
        Deletes a notification.
        :param notification_id: Notification ID
        :param kwargs:
        :return:
        """
        route = "v1/notification/delete"
        request_params = {"id": notification_id}
        return self._post_request(route=route, params=request_params, **kwargs)

    def delete_all_notifications(self, **kwargs):
        """
        Deletes all notifications.
        :param kwargs:
        :return:
        """
        route = "v1/notification/all/delete"
        data = {"id": ""}
        return self._post_request(route=route, data=data, **kwargs)


class Photo(_Parler):
    """
    Photo
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    def get_photo(self, photo_id=None, **kwargs):
        """
        Returns a photo.
        :param photo_id:  Photo ID.
        :param kwargs:
        :return:
        """
        route = "/v1/photo"
        request_params = {"id": photo_id}
        return self._get_request(route=route, params=request_params, **kwargs)


class Post(_Parler):
    """
    Post
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    def get_post(self, post_id=None, **kwargs):
        """
        Returns a post.
        :param post_id: post ID
        :param kwargs:
        :return:
        """
        route = "/v1/post"
        request_params = {"id": post_id}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_post_comments(self, post_id=None, startkey=None, limit=None, reverse=True, follow=None, **kwargs):
        """
        Returns a post's comments.
        :param post_id: post ID
        :param reverse:
        :param kwargs:
        :return:
        """
        route = "/v1/comment"
        request_params = {"id": post_id, "startkey": startkey, "limit": limit, "reverse": reverse}
        return self._get_request(route=route, params=request_params, **kwargs)

    def get_impressions(self, post_id, **kwargs):
        """
        Returns the impressions on a post.
        This method requires ownership of the target post.
        :param id: post ID
        :param kwargs:
        :return:
        """
        route = f"/v1/post/{post_id}/impressions"
        return self._get_request(route=route, **kwargs)

    @paginate
    def get_user_posts(self, post_id=None, startkey=None, follow=None, **kwargs):
        """
        Returns posts created by a user.
        :param id: User ID
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/post/creator"
        request_params = {"id": post_id, "startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_liked_posts(self, post_id=None, startkey=None, follow=None, **kwargs):
        """
        Returns posts liked by a user.
        :param post_id: post ID
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/post/creator/liked"
        request_params = {"id": post_id, "startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_creator_media(self, post_id=None, startkey=None, follow=None, **kwargs):
        """
        Returns media posted by a user.
        :param post_id: User ID
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/post/creator/media"
        request_params = {"id": post_id, "startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def search_by_hashtag(self, tag=None, startkey=None, follow=None, **kwargs):
        """
        Returns a list of posts.
        :param tag: hashtag
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/post/hashtag"
        request_params = {"tag": tag, "startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    def post(self, post, links=[], **kwargs):
        """
        Post a Parley.
        Data:
        {"body":"hello world🍆","parent":null,"links":[],"state":4}

        :param post:
        :param kwargs:
        :return:
        """
        route = "/v1/post"
        if isinstance(links, str):
            links = [links]
        data = {"body": post, "parent": None, "links": links, "state": 4}
        return self._post_request(route=route, data=data, **kwargs)

    def delete_post(self, post_id=None, **kwargs):
        """
        Delete a post.
        :param post_id: Post ID
        :param kwargs:
        :return:
        """
        route = "/v1/post/delete"
        request_params = {"id": post_id}
        return self._get_request(route=route, params=request_params, **kwargs)

    def upvote(self, post_id, **kwargs):
        """
        Updoot a post.
        :param post_id:
        :param kwargs:
        :return:
        """
        route = "/v1/post/upvote"
        data = {"id": post_id}
        return self._post_request(route=route, data=data, **kwargs)

    def rescind_upvote(self, post_id, **kwargs):
        """
        I'm officially rescinding my updoot.
        :param post_id: Post ID
        :param kwargs:
        :return:
        """
        route = "/v1/post/upvote/delete"
        data = {"id": post_id}
        return self._post_request(route=route, data=data, **kwargs)


class Profile(_Parler):
    """
    Profile
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    def get_user_profile(self, user_id=None, username=None, **kwargs):
        """
        Returns a user profile.
        :param id: User ID
        :param username:
        :param kwargs:
        :return:
        """
        route = "/v1/profile"
        request_params = {"id": user_id, "username": username}
        return self._get_request(route=route, params=request_params, **kwargs)


    def get_profile_settings(self, **kwargs):
        """
        Returns current user profile setting.
        :param kwargs:
        :return:
        """
        route = "/v1/profile"
        return self._get_request(route=route, **kwargs)

    def update_profile(self, **kwargs):
        """
        Updates the profile of the logged in user.

        Implement me!
        :param kwargs:
        :return:
        """
        # route = "/v1/profile"
        # data = {}
        # return self._patch_request(route=route, data=data, **kwargs)
        pass

    def update_profile_settings(self, **kwargs):
        """
        Updates the profile setting of the logged in user.

        Implement me!
        :param kwargs:
        :return:
        """
        # route = "/v1/profile/settings"
        # data = {}
        # return self._patch_request(route=route, data=data, **kwargs)
        pass

    def change_badge(self, **kwargs):
        """
        Implement me!
        :param kwargs:
        :return:
        """
        # route = "/v1/profile/badge/display"
        # data = {}
        # return self._post_request(route=route, data=data, **kwargs)
        pass

    def upload_cover_photo(self, file_name, **kwargs):
        """
        Upload profile cover photo.
        :param file_name: path to file
        :param kwargs:
        :return:
        """
        route = "/v1/profile/cover-photo"
        headers = {'Content-Disposition': 'form-data',
                   'Content-Type': 'image/jpeg',
                   'name': 'upload',
                   'filename': 'cover-photo.jpeg'}
        with open(file_name, 'rb') as f:
            data = f
        return self._post_request(route=route, headers=headers, data=data, **kwargs)

    def upload_profile_photo(self, file_name, **kwargs):
        """
        Upload profile photo.
        :param file_name: path to file
        :param kwargs:
        :return:
        """
        route = "/v1/profile/photo"
        headers = {'Content-Disposition': 'form-data',
                   'Content-Type': 'image/jpeg',
                   'name': 'upload',
                   'filename': 'photo.jpeg'}
        with open(file_name, 'rb') as f:
            data = f
        return self._post_request(route=route, headers=headers, data=data, **kwargs)


class User(_Parler):
    """
    User
    """

    def __init__(self, log_stdout=True, log_file=None):
        _Parler.__init__(self, log_stdout=True, log_file=None)

    @paginate
    def get_blocked_users(self, startkey=None, follow=None, **kwargs):
        """
        Returns a list of blocked users.
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/user/block"
        request_params = {"startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_users_exists(self, username=None, **kwargs):
        """
        Returns user exists status.
        :param username:
        :param kwargs:
        :return:
        """
        route = "/v1/user/exists"
        request_params = {"username": username}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_muted_users(self, startkey=None, follow=None, **kwargs):
        """
        Returns a list of muted users.
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/user/mute"
        request_params = {"startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def search_users(self, search=None, startkey=None, follow=None, **kwargs):
        """
        Search for a user by their account name.
        :param search:
        :param startkey:
        :param kwargs:
        :return:
        """
        route = "/v1/users"
        request_params = {"search": search, "startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    @paginate
    def get_suggested_users(self, startkey=None, follow=None, **kwargs):
        """
        Returns a list of suggested followers.
        :param kwargs:
        :return:
        """
        route = "/v1/users/rss"
        request_params = {"startkey": startkey}
        return self._get_request(route=route, params=request_params, **kwargs)

    def block_user(self, username, **kwargs):
        """
        Block a user.
        :param username:
        :param kwargs:
        :return:
        """
        route = "/v1/user/block"
        data = {"username": username}
        return self._post_request(route=route, data=data, **kwargs)

    def unblock_user(self, user_id, **kwargs):
        """
        Unblock a user.
        :param user_id:
        :param kwargs:
        :return:
        """
        route = "/v1/user/block/delete"
        data = {"id": user_id}
        return self._post_request(route=route, data=data, **kwargs)

    def dislike_user(self, user_id, **kwargs):
        """
        Dislike a user.
        :param user_id:
        :param kwargs:
        :return:
        """
        route = "/v1/user/dislike"
        data = {"id": user_id}
        return self._post_request(route=route, data=data, **kwargs)

    def mute_user(self, username, **kwargs):
        """
        Mute a user.
        :param username:
        :param kwargs:
        :return:
        """
        route = "/v1/user/mute"
        data = {"username": username}
        return self._post_request(route=route, data=data, **kwargs)

    def unmute_user(self, user_id, **kwargs):
        """
        Unmute a user.
        :param user_id:
        :param kwargs:
        :return:
        """
        route = "/v1/user/mute/delete"
        data = {"id": user_id}
        return self._post_request(route=route, data=data, **kwargs)

    def report(self, user_id, reason, message="", **kwargs):
        """
        Report a user.

        Data:
        {reason: "spam", message: "wow much spam", id: id}

        :param user_id:
        :param reason:
        :param message:
        :param kwargs:
        :return:
        """
        route = "/v1/user/report"
        reasons = ["spam", "terror", "ads", "slander", "blackmail", "threats", "crime",
                   "porn", "nude", "obscenity", "plagiarism", "bribe", "killing", "illegal"]
        data = {"reason": reason, "message": message, "id": user_id}
        return self._post_request(route=route, data=data, **kwargs)
