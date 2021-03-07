# Senior-Project

## python venv setup:

python3 -m venv venv

source venv/bin/activate

## Django setup:

python3 -m pip install -r requirements.txt

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py loaddata DB.json

## Run backend server

python3 manage.py runserver

## api endpoints

- /api/v1/register/
  * {POST}
    * email
    * username
    * password

- /api/v1/token/
  * {POST}
    * username
    * password

- /api/v1/token/refresh/
  * {POST}
    * refresh='JWT refresh token'

- /api/v1/me/
  * {GET}

- /api/v1/people/
  * {GET}

- /api/v1/friends/
  * {GET}
  * {POST}
    * friend='user id to add'

- /api/v1/friends/pending
  * {GET}
  * {POST}
    * friend='user id to accept'

- api/v1/videos/
  * {GET}
    * optional:
      * ?query='term'

- /api/v1/videos/\<video-id\>
  * {GET}

- /api/v1/reactions/\<video-id\>
  * {GET}
  * {POST}
    * emoji='emoji id'
    * text='text comment'
    * timestamp='video time stamp'

- /api/v1/videos/upload
  * {POST}
    * title='video title'
    * category='category id'
    * file='uploaded multipart file'

-/api/v1/categories
  * {GET}

-/api/v1/categories/\<category-id\>
  * {GET}
