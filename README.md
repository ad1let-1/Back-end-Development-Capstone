# Back-end-Development-Capstone

Djirection is a Django band website that integrates the Pictures and Songs Flask services. This project extends the [IBM Skills Network course template](https://github.com/ibm-developer-skills-network/sfvih-Back-end-Development-Capstone), licensed under Apache 2.0. The views, model fields, URL routes, migrations, and container deployment files have been completed.

## Run locally

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

On Windows, use `.venv\\Scripts\\python.exe`. Start the Songs service on port 8081 and Pictures service on port 8082 first. Override `SONGS_SERVICE_URL` and `PICTURES_SERVICE_URL` to point to deployed services. In the course workspace, the site can fall back to the adjacent seed JSON files when the services are unavailable.

## Course lab workflow

1. Clone this repository and enter its root directory.
2. Create a virtual environment and install `requirements.txt` as shown above.
3. Run `python manage.py makemigrations` to check the model state, then run `python manage.py migrate` to create the database tables.
4. Start the application with `python manage.py runserver 127.0.0.1:8000` and open `http://127.0.0.1:8000/`.
5. Use the **Songs** page to list songs and open a song's lyrics modal. Use **Photos** to see concert photographs and **Concerts** to view the seeded concert and RSVP when signed in.
6. Create an administrator with `python manage.py createsuperuser`. Choose your own username and password; do not put credentials in the repository. Open `http://127.0.0.1:8000/admin/login/`, sign in, and use Django Admin to create or edit concerts.
7. Refresh `/concerts/` to verify that the concert appears. Use `/signup/` to create a regular account and test RSVP from the public site.

Open `/` for the band home page, `/songs/` for the song list and lyric modal, `/photos/` for the photo page, `/concerts/` for a seeded concert, and `/admin/` for Django administration. A local account can be created through `/signup/`; the admin account can be created with `python manage.py createsuperuser`.

## Container and Kubernetes

```sh
docker build -t djangoserver:latest .
kubectl apply -f deployment.yml
kubectl port-forward service/djangoserver 8000:8000
```

The supplied deployment uses a local image name. A cloud cluster needs the image pushed to its registry, then the image reference and service configuration updated. Set `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` for a public deployment, and use a persistent database instead of the default SQLite file.

The featured concert photo is by [Nainoa Shizuru on Unsplash](https://unsplash.com/photos/NcdG9mK3PBY) and is included as a local static asset for reliable rendering.
