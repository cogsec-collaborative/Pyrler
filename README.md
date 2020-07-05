# Pyrler

A Parler client library in Python.

## Usage

Authenticate to Parler using the web app.  Extract the `jst` and `mst` session cookies.

Configure the session cookies as local environment variables.

`export MST_COOKIE=foo`

`export JST_COOKIE=bar`

Import the library.

`from pyrler.core import pyrler`

### Pagination

Pages are accessed via `startkey`. Each response returns `next` that is used to access the next page. The last page of data returns `last=True`.

Let's look at a user's post history.

```
# First we find the user's ID by fetching their profile. 
# username is without @.
profile = pyrler.Profile()
profile_response = profile.get_user_profile(username="")
user_id = profile_response.json()["id"]

# Store the responses in a list.
data = []
# Start with the first page of data.
startkey=None

# Then we request the paginated post history.
while True:
    p = pyrler.Post()
    r = p.get_user_posts(id=user_id, startkey=startkey)
    data.append(r.json())
    print(r.json())
    if r.json()["last"] == True:
        break
    startkey = r.json()["next"]

with open("user_parleys.json", "w") as f:
    f.write(json.dumps(data, indent=True, sort_keys=True))
```

## Methods

Take a look at `pyrler.core.pyrler.py` for the complete list of methods.

### Comment

Get a comment by its ID.
```
p = pyrler.Comment()
r = p.get_comment(id="comment_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Upvote a comment.
```
p = pyrler.Comment()
r = p.vote_comment(id="comment_id", upvote=True)
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Get all comments from user.
```
p = pyrler.Comment()
r = p.get_user_comments(id="user_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Discover

Discover recommended news.
```
p = pyrler.Discover()
r = p.discover_news()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Discover recommended users.
```
p = pyrler.Discover()
r = p.discover_users()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Discover recommended posts.
```
p = pyrler.Discover()
r = p.discover_posts()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Feed

Get the user's feed.
```
p = pyrler.Feed()
r = p.get_feed(limit=10)
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Follow

Get the user's followers.
```
p = pyrler.Follow()
r = p.get_followers(id="user_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Get the accounts a user is following.
```
p = pyrler.Follow()
r = p.get_followers(id="user_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Follow a user.
```
p = pyrler.Follow()
r = p.follow_user(username="user_name")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Hashtag

Hashtag search.
```
p = pyrler.Hashtag()
r = p.search(search="#datascience")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Identity

Check if the current user is verified.
```
p = pyrler.Identity()
r = p.get_user_verification_status()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Messaging

Get conversations.
```
p = pyrler.Messaging()
r = p.get_conversations()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Get a conversation.
```
p = pyrler.Messaging()
r = p.get_conversation(id="conversation_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Accept a conversation request.
```
p = pyrler.Messaging()
r = p.accept_conversation_request(id="conversation_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```


### Moderation

Accept a conversation request.
```
p = pyrler.Moderation()
r = p.approve_comment(id="conversation_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Filter words.
```
p = pyrler.Moderation()
r = p.filter_word(word="science", action="banUser)
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### News

Get news feed.
```
p = pyrler.News()
r = p.get_news()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Search news.
```
p = pyrler.News()
r = p.search_news(search="data science")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Notification

Get notifications.
```
p = pyrler.Notification()
r = p.get_notifications()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Delete all notifications.
```
p = pyrler.Notification()
r = p.delete_all_notifications()
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Photo

Get a photo.
```
p = pyrler.Photo()
r = p.get_photo(id="photo_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

### Post

Get a post by its ID.
```
p = pyrler.Post()
r = p.get_post(id="post_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Get the comments on a post.
```
p = pyrler.Post()
r = p.get_post_comments(id="post_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Get the posts created by a user.
```
p = pyrler.Post()
r = p.get_user_posts(id="user_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Get the posts liked by a user identified by their user ID.
```
p = pyrler.Post()
r = p.get_liked_posts(id="user_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Search post by hashtag.
```
p = pyrler.Post()
r = p.search_by_hashtag(tag="datascience")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Submit a post. Multiple links can be submitted as a Python list.
Emoji must be unicode escaped.
```
p = pyrler.Post()
r = p.post(post="Science Rules!", links="https://en.wikipedia.org/wiki/File:Bill_Nye_2017.jpg")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Upvote a post.
```
p = pyrler.Post()
r = p.upvote(id="post_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```

Delete post upvote.
```
p = pyrler.Post()
r = p.rescind_upvote(id="post_id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```


### Profile

Delete post upvote.
```
p = pyrler.Profile()
r = p.get_user_profile(id="user id")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```


### User

Get a User ID by searching their username.
```
p = pyrler.Profile()
r = p.get_user_profile(username="")
print(json.dumps(r.json(), indent=4, sort_keys=True))
```


## Credits

Copyright 2020, Cognitive Security Collaborative

API Wrapper based on code from [PyFireEye](https://github.com/EmersonElectricCo/pyFireEye).

## License

AGPLv3
