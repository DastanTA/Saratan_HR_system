# Instructions for front-end developer

## Install dependencies
 - docker
 - docker-compose
 - postman (*to check end-points*)

## Steps to run server

1. open terminal and navigate to project folder.
2. <span style="color:orange">**git checkout dev**</span> - go to dev branch
3. <span style="color:orange">**git pull origin dev**</span> - get lateset version of the branch from repo
4. <span style="color:orange">**docker-compose up -d --build**</span> - Create images for app and DB and run them
5. <span style="color:orange">**docker-compose ps**</span> - check if containers are running. "app" and "db" containers should have States "Up"
6. <span style="color:orange">**docker-compose exec app bash**</span> - opens 'terminal' of container. You are in 'app' container now.
7. <span style="color:orange">**flask db upgrade**</span> - your postgres db container now has actual tables
8. Get "<span style="color:green">HRS - Saratan.postman_collection.json</span>" from Dastan and import it to your postman
9. Check end-points. Start with 'project_type' create endpoint

If all these steps have been completed, then server is running ok. 