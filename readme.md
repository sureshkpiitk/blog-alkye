1. Install Python 3.12
2. Create venv `python -m venv venv`
3. Activate env `source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. Go to project `cd blog`
6. Run project `python manage.py runserver`
7. Register application for authentication `http://localhost:8000/o/applications/`
8. create auth token `curl --location 'http://localhost:8000/o/token/' \
--header 'client;' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'username=suresh' \
--data-urlencode 'password=123' \
--data-urlencode 'client_id=<client id>' \
--data-urlencode 'client_secret=<secret>'`

## APIs
1. Public APIs
   1. `curl --location 'localhost:8000/post/pub/'`
   2. `curl --location 'localhost:8000/post/pub/1/'`
   3. `curl --location 'localhost:8000/post/pub/comment/'`
   4. `curl --location 'localhost:8000/post/pub/comment/1/'`
   
2. Auth APIs
   1. `curl --location 'localhost:8000/post/' \
--header 'Authorization: Bearer <token>>' \
--header 'Content-Type: application/json' \
--data '{
        "title": "Some blog 5",
        "content": "hjbkdsdfvcdfvclsd",
        "auther": 1,
        "created": "2024-07-02"
}'`
   2. `curl --location --request PATCH 'localhost:8000/post/1/' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '{
    "content": "updated 1"
}'`
   3. Similar for comments

