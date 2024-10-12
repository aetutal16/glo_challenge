
---
#### Author: Andrés Tuta

---
#### Here you can find the folders with the python code, sql, documentation and more:

## Folders

- API: Here you will find the files needed to run the api. Change the .env file to include your credentials if needed.
- SQL: Here you will find the files to solve the SQL Section. Also you will find the csv files with the output generated.
- Docker Api: Here you will find the files and commands used to create the docker container with the api. Keep in mind to modify the .env file, now is pointing to the Azure postgres database.
- Documentation: Here you will find
  - User manual.
  - A pdf file with some aclarations, test cases, diagrams, etc.
  - DDL DB folder with the scripts to restore the database.

---

## About the API

- The api is running on Azure so you can access it with this link: https://appglochallenge.azurewebsites.net/
- To load files please use the route https://appglochallenge.azurewebsites.net/upload_csv/<table_name>
- There are 3 options for table names to load a file: dim_jobs, dim_departments or fact_hired_employees. For example https://appglochallenge.azurewebsites.net/upload_csv/dim_jobs

