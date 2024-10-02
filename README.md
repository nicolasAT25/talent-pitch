# TASK 1

## Tech stack
* Python
* pytest (library to automate tests)
* FastAPI (web framework for building APIs with Python based on standard Python type hints)
* Postgres/pgadmin 4 GUI (open source object-relational database system)
* Render (build, deploy, and scale apps)

## Considerations

1. In this case, data comes from a local file due to the simplicity of the files used. However, the source could be another DB or any kind of source/repository.
2. DB tables models are created with SQLAlchemy before these are populated with historical data. This creation consider rules such as FKs, not nullable fields, incremental PK for new registers. For these reasons, some PKs had to be changed from the original csv files to accomplish the tables creation rules.
3. Plese use the [FastAPI documentation](https://talent-pitch.onrender.com/docs) to prove the HTTP methods.
4. Execute first the *load_data* HTTP request for each of the tables before testing the rest of the requests.
4. Tests are made with a local test database wich have to be created previously on pgAdmin 4 (talentpitch_test).

# TASK 2

## Considerations

1. Queries were made based on the original csv files.
2. Second query in the *sql_task.ipynb* file doesn't retrive any data due to resumes' creation dates correspond to the month of June, out of the 2 months range from the current month September/October.