# Team Project
Repository of team 70dub. 
Personal contribution: practice app (giving users random programming problems, checking solutions, giving rewards), accessibility features (font size, dyslexia font). 

## Website links (inactive)
- [Production](https://team70dub.bham.team/)
- [Development](https://team70dub.dev.bham.team/)

## Prerequisites / Dependencies
- [Python v3.10.4](https://www.python.org/downloads/release/python-3104/)
> Using Python >3.10.4 features may break things.
- pip v24.0 (may already be installed by default, but if you don't have it, [here's how to get it](https://pip.pypa.io/en/stable/installation/))
- [Django v5.0.1](https://docs.djangoproject.com/en/5.0/topics/install/#installing-an-official-release-with-pip)
- SQLite (comes together with Python)
- asgiref v3.7.2
- sqlparse v0.4.2
- WhiteNoise v6.6.0
- daphne v4.1.0
- channels v4.0.0
> There's no need to install anything but Python and pip manually. All the remaining dependencies will be installed straight into your virtual environment (read the section below). 

## Virtual Environment Setup (Windows, easily adaptable for Mac/Linux with a few google searches)
1. Create a folder called `venv` in the **root directory** of the cloned repository.
2. Navigate to the `venv` folder in the terminal.
3. Run `py -3.10 -m venv .`. This should create the **virtual environment files** in `venv`.
4. **Activate** the virtual environment using `./Scripts/activate`
5. Run `pip install -r requirements.txt` to install the dependencies.
6. You can deactivate the virtual environment by running `deactivate`.
> Make sure your virtual environment is always on when you're developing.

## Django project and app setup instructions
> Note: application != an entire project. One project (i.e. website) can (and, ideally, should) have multiple applications (e.g. authentication system, blog, dashboard, etc.). To ensure best development experience, ***create a new application for each feature***.
1. Run `django-admin startproject codeplay` in repo base directory to generate the foundation:
```
codeplay/              -    root directory for the whole project
    codeplay/          -    actual Python package for the project
        __init__.py    -    empty file that indicates this directory is a Python package
        asgi.py        -    entry point for ASGI web servers
        settings.py    -    project settings/config file
        urls.py        -    project URL declarations
        wsgi.py        -    entry point for WSGI web servers
    manage.py          -    command-line utility

```
2. Run `python manage.py runserver` in the project root directory to start a local dev server on port 8000
3. Run `python manage.py startapp appname` in root directory to generate the application structure:
```
appname/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```
4. Create `urls.py` in the application directory for handing URLs.

### Additional useful steps and commands
- Run `pip install -r requirements.txt` to install dependencies via pip.
- Run `python manage.py migrate` to create any necessary DB tables for settings.INSTALLED_APPS.
- Run `python manage.py makemigrations appname` to create DB tables for each app.
- Run `python manage.py createsuperuser` to create an admin user.
- Run `python manage.py collectstatic` to dump all the static files into their special directory **(required for static files to work in deployment)**.
- Run `python manage.py check --deploy` to check if your project is ready for deployment.
- Run `$env:DJANGO_SETTINGS_MODULE="codeplay.settings.localdev"` in the VS Code terminal while in the base directory to switch to development settings.
- Run `$env:DJANGO_SETTINGS_MODULE="codeplay.settings.deploy"` in the VS Code terminal while in the base directory to switch to production settings.

## Commit Instructions
1. Only commits made to the `prod-branch` branch are pushed to prod. 
2. Your commits to the main branch will only be visible in the _dev_ environment (not prod).
3. The commits don't have to be tagged anymore.
