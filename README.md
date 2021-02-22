# Pyrler

A Parler client library in Python.

## Usage

Authenticate to Parler using the web app.  Extract the `jst` and `mst` session cookies.

Configure the session cookies as local environment variables.

`export MST_COOKIE=foo`

`export JST_COOKIE=bar`

Import the library.

`from pyrler.core import pyrler`

### Logging

Pyrler logs JSON to stdout by default. To disable stdout logging use `pyrler.Comment(log_stdout=False)`.

To log to a file use `pyrler.Post(log_file='log.txt')`.

Both stdout and file handlers can be enabled together.

### Pagination

Pyrler pulls only the first page of results by default.  To use pagination pass a truthy value to the `follow` argument.

Parler pages are indexed by `startkey` and each response returns a `next` value used to access the next page.

Let's look at a user's post history. First we find the user's `id` by fetching their profile. 
```
profile = pyrler.Profile()
profile_response = profile.get_user_profile(username="SeanHannity")
user_id = profile_response.json().get("id")
```

Now we fetch their post history starting with the first page of data.
```
p = pyrler.Post()
r = p.get_user_posts(user_id=user_id, startkey=None, follow=True)
```

You can specify the `endkey` argument to stop pagination after a certain time. `endkey` must be formatted as a timestamp (as Parler returns for its `prev`/`next` keys). For example:

```
r = p.get_user_posts(user_id=user_id, startkey=None, endkey="2021-02-16T14:53:30.429Z_322497", follow=True)
```

Note that you may still receive results earlier than `endkey` if they are on a page whose last result is _after_ `endkey`. `endkey` simply prevents pagination from continuing further back in time.

Wow. Much shitposting.

## Methods

Take a look at `pyrler/core/pyrler.py` for the complete list of methods.

Methods return a dict by default and a list of dicts when `follow=True`.

### Comment

Get a comment by its ID.
```
p = pyrler.Comment()
r = p.get_comment(comment_id="comment_id")
```

Upvote a comment.
```
p = pyrler.Comment()
r = p.vote_comment(comment_id="comment_id", upvote=True)
```

Get all comments from user.
```
p = pyrler.Comment()
r = p.get_user_comments(user_id="user_id")
```

### Discover

Discover recommended news.
```
p = pyrler.Discover()
r = p.discover_news()
```

Discover recommended users.
```
p = pyrler.Discover()
r = p.discover_users()
```

Discover recommended posts.
```
p = pyrler.Discover()
r = p.discover_posts()
```

### Feed

Get the user's feed.
```
p = pyrler.Feed()
r = p.get_feed(limit=10)
```

### Follow

Get the user's followers.
```
p = pyrler.Follow()
r = p.get_followers(user_id="user_id")
```

Get the accounts a user is following.
```
p = pyrler.Follow()
r = p.get_following(user_id="user_id")
```

Follow a user.
```
p = pyrler.Follow()
r = p.follow_user(username="user_name")
```

### Hashtag

Hashtag search.
```
p = pyrler.Hashtag()
r = p.search(search="#datascience")
```

### Identity

Check if the current user is verified.
```
p = pyrler.Identity()
r = p.get_user_verification_status()
```

### Messaging

Get conversations.
```
p = pyrler.Messaging()
r = p.get_conversations()
```

Get a conversation.
```
p = pyrler.Messaging()
r = p.get_conversation(conversation_id="conversation_id")
```

Accept a conversation request.
```
p = pyrler.Messaging()
r = p.accept_conversation_request(conversation_id="conversation_id")
```


### Moderation

Accept a conversation request.
```
p = pyrler.Moderation()
r = p.approve_comment(conversation_id="conversation_id")
```

Filter words.
```
p = pyrler.Moderation()
r = p.filter_word(word="science", action="banUser)
```

### News

Get news feed.
```
p = pyrler.News()
r = p.get_news()
```

Search news.
```
p = pyrler.News()
r = p.search_news(search="data science")
```

### Notification

Get notifications.
```
p = pyrler.Notification()
r = p.get_notifications()
```

Delete all notifications.
```
p = pyrler.Notification()
r = p.delete_all_notifications()
```

### Photo

Get a photo.
```
p = pyrler.Photo()
r = p.get_photo(photo_id="photo_id")
```

### Post

Get a post by its ID.
```
p = pyrler.Post()
r = p.get_post(post_id="post_id")
```

Get the comments on a post.
```
p = pyrler.Post()
r = p.get_post_comments(post_id="post_id")
```

Get the posts created by a user.
```
p = pyrler.Post()
r = p.get_user_posts(user_id="user_id")
```

Get the posts liked by a user identified by their user ID.
```
p = pyrler.Post()
r = p.get_liked_posts(user_id="user_id")
```

Search post by hashtag.
```
p = pyrler.Post()
r = p.search_by_hashtag(tag="datascience")
```

Submit a post. Multiple links can be submitted as a Python list.
Emoji must be unicode escaped.
```
p = pyrler.Post()
r = p.post(post="Science Rules!", links="https://en.wikipedia.org/wiki/File:Bill_Nye_2017.jpg")
```

Upvote a post.
```
p = pyrler.Post()
r = p.upvote(post_id="post_id")
```

Delete post upvote.
```
p = pyrler.Post()
r = p.rescind_upvote(post_id="post_id")
```


### Profile

Delete post upvote.
```
p = pyrler.Profile()
r = p.get_user_profile(user_id="user_id")
```


### User

Get a User ID by searching their username.
```
p = pyrler.Profile()
r = p.get_user_profile(username="")
```

## Network 

If you've collected some Parler post data, you can create a network of their mentions in Gephi with: 
```
pyrler/utilities/network.py data.jsonl network_of_data.gexf
```
Create a network of their hashtags. 
```
pyrler/utilities/network.py --hashtags data.jsonl network_of_data.gexf
```
Create a network of their echos.
```
pyrler/utilities/network.py --echo data.jsonl network_of_data.gexf
```
Additionally if you want to convert the network into a dynamic network with timeline enabled (i.e. nodes will appear and disappear according to their  attributes), you can open up your GEXF file in Gephi and follow [these instructions](https://seinecle.github.io/gephi-tutorials/generated-html/converting-a-network-with-dates-into-dynamic.html). Note that in network_of_data.gexf there is a column for "start_date" (which is the day the post was created) but none for "end_date" and that in the dynamic timeline, the nodes will appear on the screen at their start date and stay on screen forever after.  For the "Time Interval creation options" pop-up in Gephi, the "Start time column" should be "start_date", the "End time column" should be empty, the "Parse dates" should be selected, and the Date format should be the last option, "dd/MM/yyyy HH:mm:ss".

## Credits

Copyright 2020, Cognitive Security Collaborative

## License

AGPLv3
