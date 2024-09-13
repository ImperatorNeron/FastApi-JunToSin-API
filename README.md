# JunToSin API

## Overview

**JunToSin API** provides a reliable backend engine for a startup that aims to help newbies find their first free commercial experience and veterans to reduce their workload. The API is built using Fast API and SQLAlchemy with asynchronous approach.

## Requirements
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)


## How to Use

1. Clone the repository:
```bash
git clone https://github.com/ImperatorNeron/FastApi-RestoMenu-Api.git
cd your_repository
```
2. Install all required packages in **Requirements** section.

### Implemented Commands

#### Application
- ```make app``` - up application
- ```make app-logs``` - follow the logs in app container
- ```make app-down``` - down application and all 
#### Storages
- ```make storages``` - up PostgreSql
- ```make storages-logs``` - follow the logs in postgres container
- ```make storages-down``` - down PostgreSql
#### Migrations
- ```make migrations``` - do alembic revision
- ```make auto-migrations``` - do alembic revision with autogenerate
- ```make migrate-up``` - do migrations (to head)
- ```make migrate-down``` - do migrations downgrate (-1)
## License

This project is licensed under the MIT License - see the [LICENSE](https://en.wikipedia.org/wiki/MIT_License) file for details.