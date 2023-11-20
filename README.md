

## Manual Build / DEV

> Download code

```bash
$ git clone olfloramanager
$ cd olfloramanager
```
 
> Install Node Modules 

```
$ npm i
$ npm run build
```

> Install **Django** modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

> set sqlite for local database in settings.py


> Install **Tailwind/Flowbite** (separate terminal)

```bash
$ npm install
$ npm run dev        
```

> Migrate DB

```
$ python manage.py makemigrations
$ python manage.py migrate
```

> Create Superuser & Start the APP

```
$ python manage.py createsuperuser # create the admin
$ python manage.py runserver       # start the project
```

<br />

## Start With Docker / Production

> Download code

```bash
$ git clone olfloramanager
$ cd olfloramanager
```

> Start with Docker Compose

```bash
$ docker-compose up --build 
``` 

Visit the app in the browser `localhost:5085`.

<br />


