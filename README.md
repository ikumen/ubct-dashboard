# Udacity Bertelsmann TS Cloud Track Data API

Data provider for scholars enrolled in [Udacity Bertelsmann Tech Scholarship Cloud Track](https://www.udacity.com/bertelsmann-tech-scholarships) challenge course, consume it and build something cool.

* [Overview](#overview)
* [Data API](#data-api)
  - [Security](#security)
  - [Data and API Endpoints](#data-and-api-endpoints)
* [Quick start](#quick-start)


## Overview

What does it do? In simple terms: takes in data generated from the Udacity Bertelsmann TS Cloud Track community of scholars, loads it into a SQL Database then provides the data via API for apps developed by our community of aspiring scholars to consume. The goal is to showcase how various Azure services can be utilized to implement the following architecture.

```                
                       |             Azure Cloud
                       |      +----------------+
                       | +--->|  Blob Storage  |<--------------+
+----------------+     | |    +-------|--------+               |
|   User Data    |     | |    +-------v--------+      +--------V--------+
|  from various  |-----^-+--->|  Azure Event   |----->| Azure Functions |  
|    sources     |     |      |     Grid       |      +--------+--------+
+----------------+     |      +----------------+               |     
                       |                                       |
                       |      +----------------+     +---------v----------+
+------------+         |      | UBTS Data API  |     | Azure SQL Database |
| +----------+-+       |      | (App Service)  |     +---------+----------+
| |  Awesome   |       |      |                |<--------------+
| |   Apps     |<------^------| /students      |
+-|            |       |      | /messages      |     +--------------------+
  +------------+       |      +--------+-------+     | Microsoft Identity |
        ^--------------^---------------^-------------|      Platform      |
                       |                             +--------------------+
                       |
```

### Core Components

The functional scope of the project covers the components listed under the Azure cloud section, how those components injest data, and how they integrate with one another. 

- [Azure Blob storage]() less frequently updated data are published to a blob container, then picked up via Event triggered Function for ingesting into our database
- [Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/) frequently updated data is published to our Event Grid and queued for processing
- [Azure Functions](https://azure.microsoft.com/en-us/services/functions/) are triggered by our Event Grid to take the data and insert/updates to our SQL Database
- [Azure SQL Database](https://docs.microsoft.com/en-us/azure/azure-sql/database/) our data store
- UBTS Cloud Track Data API (via [Azure App Services](https://azure.microsoft.com/en-us/services/app-service/)) app, exposes the data for consuming apps

#### UBTS Cloud Track Data API

The UBTS Cloud Track Data API application consists of two app modules: 1) a dashboard for users to register their applications and acquire an API key and 2) the API server.

<img src="docs/ubtsct-login.png" width="200"/> <img src="docs/ubtsct-verify.png" width="200"/> <img src="docs/ubtsct-dashboard.png" width="200"/> <img src="docs/ubtsct-dashboard2.png" width="200"/>


## Data API

### Security

Access to the API is granted in two steps, the first being an [OAuth authorization code flow](https://auth0.com/docs/flows/authorization-code-flow) to an external OAuth provider. After the OAuth provider has identified the user, we then verify the user is a scholar of Udacity/Bertelsmann TS Cloud Track with a simple Slack user challenge&mdash;note this verification only needs to be performed once on initial sign in. For subsequent sign ins, we rely on trust that the OAuth provider is sending us back the same user, of which we have already verified from the initial sign in.

If you look at our sequence diagram below, you'll notice steps 1-8 are like any other [OAuth authorization code flow](https://auth0.com/docs/flows/authorization-code-flow). Steps 9-10 is our custom Slack user challenge.

9) if the user returned from an OAuth provider in step 8 is new, we given them a short live token and ask them to publish this token as a [Slack snippet](https://slack.com/help/articles/204145658-Create-a-snippet)
10) we then verify the publish snippet contains the token, thus confirming they are a member of our community of scholars

```             
[ User ]     [UBTSCT Data API]   [OAuth Provider]    [UBTSCT Slack Workspace]
    |               |                    |                  |
 (1)|-------------->|                    |                  |
    |            (2)|------------------->|                  |
    |<--------------^--------------------|(3)               |
 (4)|---------------^------------------->|                  |
    |               |<-------------------|(5)               |
    |            (6)|------------------->|--+               |
    |               |                    |  |(7)            |
    |               |<-------------------|--+               |
    |<--------------|(9)                 | (8)              |
    |               |                    |                  |
    |               |<-------------------^----------------->|
    |               |       (10)         |                  |
```

Once the user has access to the API, they can register an application and receive an API key that must be sent along with every request to the API.

### Endpoint Authentication

All requests to `/api/resource/*` endpoints require an "Authorization" header with the API key obtained during application registration (above) as the value.

```
Authentication: <your API key>
```

### Data and API Endpoints

The API offers the following data sets and their respective endpoints.

#### Slack Users

| Endpoint | `/api/resource/slack/users` |
| :-- | :-- |
| __Method__ | GET |
| __Description__ | List of Slack users |
| __Parameters__ | <ul><li>`page` _number_ optional, defaults to 1</li><li>`per_page` _number_ optional, defaults to 10, valid range10 <= n <= 100</li><li> `tz_offset` _string_ optional, filter user by time zone offset from GMT, example format UTC+03:00</li></ul>  |

Example request and response to `/api/resource/slack/users`

* Request
  ```bash
  http <ubtsct-uri>/api/resource/slack/users Authorization:xOZWX3KofjPQ4jjr6MV6sP7BhiEglz2jzmiWg tz_offset==UTC+03:00 per_page==10
  ```
* Response
  ```bash
  {
  "items":[
    {"id":"U0001UBTSCT","name":"Arthur","avatarId":"abcdef123451","fullName":"Terry Gilliam","title":"","offset":"UTC+03:00"},
    {"id":"U0002UBTSCT","name":"Badger","avatarId":"abcdef123452","fullName":"Eric Idle","title":"","offset":"UTC+03:00"},
    ...
   ],
   "page": 1,
   "per_page": 10,
   "total": 87
  }
  ```

#### Slack Channels

Slack channels belonging to the cloud track (updated daily to Blob storage)

[[TODO]]

#### Slack Messages

Slack messages for each channel in the cloud track (throughout day to Event Grid)

[[TODO]]


## Quick Start

If you're looking to extend/customize/contribute or simply demo this project, here's a quick start. 

You should have the following installed:

- [Python 3.7 or later](https://www.python.org/downloads/)
- [pyenv](https://github.com/pyenv/pyenv) (it's not needed, but makes life easier if you need to switch between Python versions)
- [Docker](https://docs.docker.com/get-docker/)
- [sqlcmd](https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility?view=sql-server-ver15)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- and an IDE would be helpful ([Visual Studio Code is nice](https://code.visualstudio.com/)).

### Configurations

Configuration is modeled after [12-factor](https://12factor.net/) practices, all configurations are either declared directly in [settings.py](/backend/settings.py) or read from environment variables. On Azure, we'll use [App Service configurations](https://docs.microsoft.com/en-us/azure/app-service/configure-common). Locally we use [python-dotenv](https://github.com/theskumar/python-dotenv) to load a local `.env` file containing all the local configurations, including secrets. This local configuration file should not be checked into source control, so an [entry to have it ignored already exists in `.gitignore`](/.gitignore#L105)

#### Setting Up OAuth Providers

Microsoft/Azure 

1. Azure Active directory -> App registrations (left hand pane) 
1. New registration
  - Name: (e.g, myapp-api, myapp-api-development)
  - Account Types: choose in any organization (multitenant)
  - Redirect: http://localhost:5000/oauth/azure/success
1. Upon completion, go to resouce -> Certificates & secrets (left hand pane)
  - New client secret (take note of client secret and key)

GitHub


- config
- build
- deploy

