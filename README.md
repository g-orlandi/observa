# observa

Author: Giovanni Orlandi  
A.A: 2024-2025  

# Observa

Observa is a web-based monitoring platform developed as part of a **Web Technologies exam** during a BSc in Computer Science.

The system provides a unified view of server, web service, and backup supervision by aggregating heterogeneous monitoring metrics and presenting them through interactive, time-series–based dashboards.

Observa acts as a presentation layer on top of existing monitoring tools, delegating data collection and storage to Prometheus and related services, while offering a normalized and user-friendly interface for system administrators.

## Main features

- Monitoring of web endpoints availability and response times
- Supervision of remote servers (CPU, memory, disk usage)
- Monitoring of backup servers and incremental backup status
- Time-series visualization with multiple levels of granularity
- Free and Pro usage levels with different monitoring capabilities

## Technology stack

- Backend: Django (Python)
- Frontend: HTML, JavaScript, HTMX
- Monitoring & metrics: Prometheus
- Backup monitoring: Restic
- Uptime monitoring: Uptime Kuma


---

Use: Python >= 3.12

## Manual provisioning on local development machine

Create environment for new project:

```bash
cd ~/Projects/
mkdir observa
mkdir observa/public
mkdir observa/public/static
mkdir observa/public/media
```

Create and activate a virtualenv for the project:

```bash
mkvirtualenv observa
workon observa
```

or

```bash
mkdir ~/.virtualenvs
python3 -m venv ~/.virtualenvs/observa
```

to be activated later as follows:

```bash
source ~/.virtualenvs/observa/bin/activate
```

Clone source repository:

```bash
cd /Projects/observa/
git clone git@gitlab.com:univeristy3/observa.git
```

The final project layout is:

```
    .
    ├── observa
    │   ├── README.md
    │   ├── ...
    │   ├── manage.py
    │   ├── main          <---- this is the Django project
    │   ├── requirements
    │   └── ...
    └── public
        ├── media
        └── static
```

Update the virtualenv (that is: Install required python packages):

```bash
cd /Projects/observa/observa/
pip install -r requirements/development.txt
```

Create a local settings file;
for example, copy and adapt "local_example.py":

```bash
cd /Projects/observa/observa/
cp main/settings/local_example.py main/settings/local.py
```

Create database (use database name and password specified in local.py):

```bash
psql
create user observa with password '<PASSWORD>';
create database observa owner observa;
```

Populate database struct:

```bash
python manage.py migrate
```

Update front-end assets:

```bash
npm install
```

Create a supersuser account and run the development server:

```bash
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

---

## Development workflow

```bash
cd /Projects/observa/observa
workon observa
or:
source ~/.virtualenvs/observa/bin/activate
git pull
pip install -r requirements/development.txt
python manage.py migrate
npm install
python manage.py runserver
```
