# TUITER - DJANGO REST API
## Introduction
This API was made for learning purposes. The idea was based on the basic functionality of Twitter. Registered users can post content, such as text or an image, in their own profiles. They can also follow other users and comment on their posts, share them or add them to their liked content list.  
Every GET request that returns a list is paginated and has the same format. For example, a list request of profiles would be: http://localhost:8000/accounts/profile-list/  
And the response would have the following format:
```json
{
    "count": 23,
    "next": "http://localhost:8000/object-list/?page=12",
    "previous": "http://localhost:8000/object-list/?page=10",
    "results": [
        {
            ...
        },
        {
            ...
        },
        ...
    ]
}
```
"count" is the total profiles, "results" is a list of profiles per page (10 profiles max), "next" is the url to the next page (would be null in the last page) and "previous" the url of the previous page (would be null in the first page).

## Endpoints

**/accounts/registration/**
>Creates the user and sends an e-mail with a url to activate the account.
* Methods: POST
* Parameters:
  - email
  - username
  - password1
  - password2
#
**/accounts/registration/account-confirm-email/**```:key:```**/**
>This is the url sent via e-mail to activate the account.
* Methods: GET
* Parameters:
    - key

#
**/accounts/login/**
>A user can login providing either username or email.
* Methods: POST
* Parameters:
    - username
    - email
    - password
* Example Response:
```json
{
    "key": "bfadbe76a5e67f0929822e1633c41e7882edca5d"
}
```
#
**/accounts/logout/**
* Methods: POST

#
**/accounts/password/reset/**
>Sends an e-mail to the email address, provided by the user, with a url to reset the password. 
* Methods: POST
* Parameters:
    - email

#
**/accounts/password-reset/confirm/**```:uid:```**/**```:token:```**/**
>This is the url sent via e-amil to reset the password. Url parameters ("uid" and "token") must also be sent in the body of the request, only in this endpoint. In other endpoints, url parameters shouldn't be sent in the body of the request, unless the otherwise stated.
* Methods: POST
* Parameters:
    - uid
    - token
    - new_password1
    - new_password2

#
**/accounts/password/change/**
>Change the password (requires authentication).
* Methods: POST
* Parameters:
    - old_password
    - new_password1
    - new_password2

#
**/accounts/user/**
>Shows your user detail, and allows to modify the username, first name and last name (requires authentication).
* Methods: GET, PUT, PATCH
* Parameters:
    - username
    - first_name
    - last_name
* Example Response:
```json
{
    "pk": 1,
    "username": "admin",
    "email": "admin@django.com",
    "first_name": "",
    "last_name": ""
}
```
#
**/accounts/profile/**```:username:```**/**
>Shows a specific profile detail. If a profile is private, its "followers", "following", "mainPostList" and "likedPostList" will be visible only for the users that are being followed by the owner of the private profile.
* Methods: GET
* Parameters:
    - username
* Example Response:
```json
{
    "id": 1,
    "user": "admin",
    "fullname": "El Administrador",
    "description": "I'm a Django REST developer",
    "profilePicture": null,
    "isPrivate": true,
    "birthdate": "1997-10-21",
    "followersCount": 3,
    "followingCount": 1,
    "followers": "http://localhost:8000/accounts/profile/admin/followers/",
    "following": "http://localhost:8000/accounts/profile/admin/following/",
    "mainPostList": "http://localhost:8000/postings/main-post-list/admin/",
    "likedPostList": "http://localhost:8000/postings/liked-post-list/admin/"
}
```
#
**/accounts/profile/**```:username:```**/followers/**
>List of followers(profiles) of a specific user.
* Methods: GET
* Parameters:
    - username
* Example Response:
```json
{
    "count": 125,
    "next": "http://localhost:8000/accounts/profile/user_example/followers/?page=12",
    "previous": "http://localhost:8000/accounts/profile/user_example/followers/?page=10",
    "results": [
        {
            "id": 7,
            "user": "another_user555",
            "fullname": "User 555",
            "description": "",
            "profilePicture": null,
            "isPrivate": true,
            "birthdate": "2020-04-02",
            "followersCount": 1,
            "followingCount": 1,
            "followers": "http://localhost:8000/accounts/profile/another_user555/followers/",
            "following": "http://localhost:8000/accounts/profile/another_user555/following/",
            "mainPostList": "http://localhost:8000/postings/main-post-list/another_user555/",
            "likedPostList": "http://localhost:8000/postings/liked-post-list/another_user555/"
        },
        ...
        ...
        ...
    ]
}
```
#
**/accounts/profile/**```:username:```**/following/**
>List of users(profiles) that a specific user follows.
* Methods: GET
* Parameters:
    - username

#
**/accounts/profile/**```:username:```**/follow/**
>This endpoint is used to follow or unfollow another user (requires authentication).
* Methods: POST, DELETE
* Parameters:
    - username
#
**/accounts/profile/**```:username:```**/update/**
>Updates your profile, so the "username" parameter in the url should be your own username, you won't be able to update someone else's profile (requires authentication). Max lenghts: fullname = 30, description = 200. Birthdate format = YYYY-MM-DD
* Methods: PUT
* Parameters:
    - fullname
    - description
    - profilePicture
    - isPrivate
    - birthdate

#
**/accounts/profile-list/**
>Whole list of profiles. You can search by "username" or "fullname" adding "?search=your_search" at the end of the url. For example: http://localhost:8000/accounts/profile-list/?search=admin
* Methods: GET
* Search fields: 
    - username
    - fullname


#
**/postings/create-post/**
>Creates a user post (this would be like a tweet). All the parameters are optional. If you want to send a comment, "mainPost" must be the id of the post that you are commenting on. If you want to share a post, "rePost" must be the id of the post that you want to share. Text's max lenght is 300. (Requires authentication)
* Methods: POST
* Parameters:
    - text
    - image
    - mainPost
    - rePost
#
**/postings/post-detail/**```:post_id:```**/**
>Detail of a specific post.
* Methods: GET, DELETE
* Parameters: 
    - post_id
* Example Response:
```json
{
    "id": 5,
    "user": "ThirdUser99",
    "timestamp": "2020-04-04T20:11:54.634346-03:00",
    "text": "This is a comment!",
    "image": null,
    "likesCount": 0,
    "sharedCount": 0,
    "mainPost": 13,
    "rePost": null,
    "comments": "http://localhost:8000/postings/post-detail/5/comments/",
    "usersThatLiked": "http://localhost:8000/postings/post-detail/5/likes/",
    "usersThatShared": "http://localhost:8000/postings/post-detail/5/shared/"
}
```
#
**/postings/post-detail/**```:post_id:```**/like/**
>Used to like a post. A POST request will add the post (or "tweet") to your liked content list in your profile. A DELETE request will remove the like.
* Methods: POST, DELETE
* Parameters:
    - post_id

#
**/postings/post-detail/**```:post_id:```**/users-that-liked/**
>List of users (profiles) that liked a specific post.
* Methods: GET
* Parameters:
    - post_id

#
**/postings/post-detail/**```:post_id:```**/users-that-shared/**
>List of users (profiles) that shared a specific post.
* Methods: GET
* Parameters:
    - post_id

#
**/postings/post-detail/**```:post_id:```**/comments/**
>List of posts that are comments of a another specific post.
* Methods: GET
* Parameters:
    - post_id

#
**/postings/index-main-post-list/**
>List of main posts (not comments) sent by users that you follow.
* Methods: GET

#
**/postings/main-post-list/**```:username:```**/**
>List of main posts (not comments) of a specific user.
* Methods: GET
#
**/postings/liked-post-list/**```:username:```**/**
>Liked content (main posts or comments) of a specific user.
* Methods: GET
* Successful response: list of posts liked by a specific user.
