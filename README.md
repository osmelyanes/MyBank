# MyBank Test Project

## Software requirements
- Python 3.X
  ```
  https://www.python.org/
  ```
- Docker 3.x  
  ```
  https://www.docker.com/
  ```

## Deployment instructions

### Build automation with Docker 
- Make sure you have ```Docker Compose``` installed
  ```
  https://docs.docker.com/compose/install/
  ```

- Find ```docker-compose.yml``` inside root folder and run the following command from the same directory
  ```
  docker-compose up --build
  ```

Docker will create and start required services to get the app ready
- The ```db``` service is available at ```localhost:5433```
- The ```app``` service is available at ```localhost:8001```

Once the initialization is finished browse the following link to access the project
  ``` 
  http://localhost:8001
  ``` 

In addition, some fixtures were run to have some sample data for easing the review 
- The sample data is linked to Django ```superuser```
- The sample data is visible using the following credentials ```[admin:admin]```

Django Admin is also available and sample data can be managed navigating to Account.Person model once logged in 
  ``` 
  http://localhost:8001/admin
  ``` 

### Manual setup
- Make sure you have ```Python``` installed
  ```
  https://realpython.com/installing-python/
  ```

- Install the requirements list
  ```
  pip install -r requirements.txt
  ```

- Create db structure and run the app service assuming db service is ready 
  ```
  python manage.py migrate
  python manage.py collectstatic
  python manage.py runserver
  ```
  
- Once the initialization is finished browse the following link to access the project
  ``` 
  http://localhost:8001
  ``` 

Refer to the automation build with Docker for more details
<br>
Find starting Django Admin credentials as well as other specifications


## Running tests
```
python manage.py test Account
```

## Further enhancements
- Add Bootstrap to improve user experience 
- Replace Django development web server by Nginx web server
- Cover with more tests the solution due to not all test cases were implemented
- Create distinct environments for development and production rather than using a single one