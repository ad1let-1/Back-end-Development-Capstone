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

Open `/` for the band home page, `/songs/` for the song list and lyric modal, `/photos/` for the photo page, `/concerts/` for a seeded concert, and `/admin/` for Django administration. A local account can be created through `/signup/`; the admin account can be created with `python manage.py createsuperuser`.

## Container and Kubernetes

```sh
docker build -t djangoserver:latest .
kubectl apply -f deployment.yml
kubectl port-forward service/djangoserver 8000:8000
```

The supplied deployment uses a local image name. A cloud cluster needs the image pushed to its registry, then the image reference and service configuration updated. Set `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` for a public deployment, and use a persistent database instead of the default SQLite file.

The featured concert photo is by [Nainoa Shizuru on Unsplash](https://unsplash.com/photos/NcdG9mK3PBY) and is included as a local static asset for reliable rendering.
