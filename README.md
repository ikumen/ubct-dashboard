# Udacity / Bertelsmann Tech Scholarship Cloud Track Data API

Data provider for scholars enrolled in [Udacity/Bertelsmann Tech Scholarship Cloud Track](https://www.udacity.com/bertelsmann-tech-scholarships) challenge course&mdash;ingest it and build something cool.

* [Overview](#overview)
  - [Core components](#core-components)
  - [User data](#user-data)
  - [API endpoints](#api-endpoints)
* [Quick start](#quick-start)
* [How we built it](#how-we-built-it)


## Overview

What does it do? In simple terms: takes in data generated from the Udacity/Bertelsmann TS Cloud Track community of scholars, loads it into a SQL Database and in turns provides the data via API for apps developed by our community of aspiring scholars to consume. The goal is to showcase how various Azure services can be utilized to implement the following architecture.

```                
                    |         Azure Cloud
+--------------+    |    
|  User Data   |    |    +--------------+     +-----------------+
| from various |----^--->| Azure Event  |---->| Azure Functions |  
|   sources    |    |    |    Grid      |     +--------+--------+
+--------------+    |    +--------------+              |     
                    |                                  |
                    |   +---------------+    +---------v----------+
+-----------+       |   | UBCT Data API |    | Azure SQL Database |
| +---------+-+     |   | (App Service) |    +---------+----------+
| |  Awesome  |     |   |               |<-------------+
| |   Apps    |<----^---| /students     |
+-|           |     |   | /messages     |    +--------------------+
  +-----------+     |   +-------+-------+    | Microsoft Identity |
        ^-----------^-----------^------------|      Platform      |
                    |                        +--------------------+
```

### Core Components

The functional scope of the project covers the components listed under the Azure cloud section, how those components injest data, and how they integrate with one another. 

- [Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/) ingest student data from a source publisher and queue it for processing
- [Azure Functions](https://azure.microsoft.com/en-us/services/functions/) takes the ingested data and insert/updates to our SQL Database
- [Azure SQL Database](https://docs.microsoft.com/en-us/azure/azure-sql/database/) our data store
- UBCT Data API (via [Azure App Services](https://azure.microsoft.com/en-us/services/app-service/)) is a webapp that exposes the data for consuming apps

### User Data

For the user generated (_how it's generated is not in scope for this project_) data, we can expect the following sources, publish to our system intermittently throughout the day.

#### Slack 

- users belonging to the cloud track
- channels belonging to the cloud track
- messages for each channel in the cloud track

### API Endpoints

For this phase of the project, the following endpoints are supported.

[[TODO]]

#### Security

Access to the API will be protected using a combination of OAuth and a simple Slack user challenge. 

## Quick Start

If you're looking to extend/customize/contribute or simply demo this project, here's a quick start. The project is based on our [Azure Flask Starter](https://github.com/ikumen/azure-flask-starter), so it might be easier to familiarize yourself with that app to see how the project structure is laid out. 

You should have the following installed:

- [Python 3.7 or later](https://www.python.org/downloads/)
- [pyenv](https://github.com/pyenv/pyenv) (it's not needed, but makes life easier if you need to switch between Python versions)
- [Docker](https://docs.docker.com/get-docker/)
- [sqlcmd](https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility?view=sql-server-ver15)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- and an IDE would be helpful ([Visual Studio Code is nice](https://code.visualstudio.com/)).

[[TODO]]
- config
- build
- deploy


### Azure CLI Cheat Sheet

#### Login
```bash
# You'll need to explicitly specify a tenant id if you MFA enabled
az login --tenant <tenant_id>
```

#### Creating Resouce Group
```bash
az group create -n <resource-group-name> -l westus2
```



