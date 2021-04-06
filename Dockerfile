FROM ubuntu

MAINTAINER <martha.dybas@ryerson.ca>

RUN apt-get update

RUN apt-get install nginx -y

COPY index.html /var/www/html/

CMD ["nginx", "-g" ,"daemon off;"]

//docker run -d --name a2cps847 -p 8000:80 e39a13a95f93 -->start running
//docker ps --> check if it's running
//http://localhost:8000 -->see "Hello World"
