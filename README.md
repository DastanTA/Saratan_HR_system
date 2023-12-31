## Global configs 
These are needed to be installed on the machine. 
- Python version 3.10.6
- Postgres version 14 [psql (PostgreSQL) 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)]
- Docker version 24.0.5, build ced0996 


## Docker commands:
  - **docker build -t hrs_main_docker .**   *[builds our image gives it a name(tag= -t)]*
  - **docker run -dp 5000:5000 hrs_main_docker** *[initiates the container using the indicated image (in prod)]*
  - **docker ps -a**  *[shows status of all containers]*
  - **docker kill {hash of container}**  *[stops the container]*
  - **docker start {hash of container}**  *[restarts the container]*
  - **docker rm {hash of container}**  *[removes the container]*
  - **docker run -dp 5000:5000 -w /app -v "$(pwd):/app" hrs_main_docker**     *[run docker locally on Linux(in dev)]*
  - **docker run -dp 5000:5000 -w /app -v "/c/Documents/yourproject:/app" hrs_main_docker**     
    - *[run docker locally on Windows(in dev)]*. 
    - > *Instead of /c/Documents/yourproject, use the path to your project (but remember to use /c/ instead of C:/)*.


## Docker-compose commands:
  - **docker-compose up -d --build**   *[builds our images then runs containers on background]*
  - **docker-compose down** *[stops containers without deleting volumes]*
  - **docker-compose down -v** *[stops containers and deletes volumes]*
  - **docker-compose exec app bash** *[enter the 'app' container with bash]*
  - **docker-compose exec db psql -U hrs_db** *[enter 'db' container with psql under user hrs_db (by default to database hrs_db)]*



## Data base:
 - usefull link to create user and db in postgres (commands): https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart
 - database name: "hrs_db"
 - postgres user to use the database: "hrs_db"
 - password for "hrs_db" user: "hrs_db"
