#docker note

In the Dockerfile, I first copied requirements.txt before pip install and app.py just like in drill 2. I used this order so docker wont have to reinstall psycopg every time there is a rebuild and make future updates faster.

#compose note
In the Compose file db is used as the name, since i wanted it to use db instead of localhost. the PostgreSQL container also have a healthcheck just like from the previous drills it has a depends_on and condition: service_healthy. there is also a volume named db_data so data will always exist even if containers are deleted. the password Rene-Bituin-ng-Mindanao is just a random password

# fourth column of prediction sheet

I made a lot of mistakes while doing this since I struggled at making the JSON work. As for the App.py i just used the skeleton of Drill4 since based on my understanding on the BUILD.md it will look somehow similar. I tried testing the functionality of the app.py using curl somehow it returned as working and returned some values