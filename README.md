# DataOps Utility Service

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.7](https://img.shields.io/badge/python-3.7-green?style=for-the-badge)](https://www.python.org/)


This service contains dataops that should not have access to greenroom. It's built using the FastAPI python framework.

## Installation

### Install requirements

`pip install -r requirements.txt`

Run the service with uvicorn
`python app.py`

### Docker

*docker-compose*

`docker-compose build`
`docker-compose up`

*Plain old docker*

`docker build . -t service_data_ops`
`docker run service_data_ops`






