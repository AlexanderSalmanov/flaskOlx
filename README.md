# flaskOlx

Flask-based Python application which allows browsing the advertisements directly from OLX. <br>
Currently, category filtration and keyword search + pagination of the results are implemented. <br>
Previously discovered results are stored in PostgreSQL database, so that they are not repeatedly pulled from OLX when searching by the same category/keyword.

## Tech stack
- Python;
- Flask;
- requests;
- BeautfilSoup4;
- PostgreSQL;
- Docker

## Prerequisites
- Git CLI;
- Docker/Docker Desktop installed on your local machine.

## Local installation steps
1. Clone this repo to the desired directory: `git clone <repo_link>`;
2. Navigate to the `flaskOlx` subdirectoryL `cd flaskOlx`;
3. Copy the contents of `src/.env.example` to `.src/.env`;
4. Build the project with `docker-compose build`;
5. Run the project with `docker-compose up`;
6. Open your browser and go to `localhost:5000`;
7. Enjoy!
