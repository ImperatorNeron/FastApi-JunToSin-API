# JunToSin API

## Overview

**JunToSin API** provides a reliable backend engine for a startup that aims to help newbies find their first free commercial experience and veterans to reduce their workload. The API is built using Fast API and SQLAlchemy with asynchronous approach.

## Requirements
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/) or [Scons](https://pypi.org/project/SCons/)


## How to Use

1. Clone the repository:
```bash
git clone https://github.com/ImperatorNeron/FastApi-RestoMenu-Api.git
cd your_repository
```
2. Install all required packages in **Requirements** section.

### Implemented Commands

#### Application
Choose make or scons:
- ```make\scons up``` - up application
- ```make\scons logs``` - follow the logs in app container
- ```make\scons down``` - down application and all 
#### Storages
- ```make\scons storages``` - up PostgreSql
- ```make\scons storages-logs``` - follow the logs in postgres container
- ```make\scons storages-down``` - down PostgreSql
#### Migrations
- ```make\scons migrations``` - do alembic revision
- ```make\scons auto-migrations``` - do alembic revision with autogenerate
- ```make\scons migrate-up``` - do migrations (to head)
- ```make\scons migrate-down``` - do migrations downgrate (-1)
## License

This project is licensed under the MIT License - see the [LICENSE](https://en.wikipedia.org/wiki/MIT_License) file for details.