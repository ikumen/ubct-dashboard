# Udacity Bertelsmann TS Cloud Track Data API

Data provider for scholars enrolled in [Udacity Bertelsmann Tech Scholarship Cloud Track](https://www.udacity.com/bertelsmann-tech-scholarships) challenge course, consume it and build something cool.

* [Overview](#overview)
* [Data API](#data-api)
  - [Security](#security)
  - [API Endpoints](#api-endpoints)
* [Production](#production)
* [Development](#development)
  - [Configuration](#configuration)
  - [Build and Run](#build-and-run)


## Overview

What does it do? In simple terms: takes data from the Udacity Bertelsmann TS Cloud Track community of scholars, loads it into a SQL Database, then provides the data via an API for our community of scholars to consume. The goal is to showcase how various Azure services can be utilized to implement the following architecture.

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

The UBTS Cloud Track Data API is a Flask app with two modules, the API server and a SPA user dashboard for managing applications and API keys.

##### SPA User Dashboard

<img src="docs/ubtsct-login.png" width="300"/> <img src="docs/ubtsct-verify.png" width="300"/> <img src="docs/ubtsct-dashboard.png" width="300"/> <img src="docs/ubtsct-dashboard2.png" width="300"/>


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

#### Endpoint Authentication

All requests to `/api/resource/*` endpoints require an "Authorization" header with the API key obtained during application registration (above) as the value.

```
Authentication: <your API key>
```

### API Endpoints

Requests that return lists of items will be paginated. You can customize how the results are paged back with the following parameters.

| Parameter | Type | In | Description |
| :-- | :-- | :-- | :-- |
| `page` | integer | query | (optional) the page to return, defaults to 1, invalid page will return 404 |
| `per_page` | integer | query | (optional) the page size, defaults to 100, valid range 10 <= size <= 100 |

A typical paginated response looks like this, `items` will contain the resource items being returned.
```json
{
  "items": [{...}, ],
  "page": 1,
  "per_page": 100,
  "total": 2000
}
```

The API offers the following data sets and their respective endpoints. 

#### List Slack Users

List all Slack users, sorted by name.

```
[GET] /api/resource/slack/users
```
##### Parameters
| Name | Type | In | Description |
| :-- | :-- | :-- | :-- |
| `tz_offset` | string | query | (optional) only show users with given time zone offset from GMT. Format expected: `UTC+03:00` |

##### Example Request

* [httpie](https://httpie.io/)
  ```bash
  http <ubtsct-uri>/api/resource/slack/users Authorization:xOZWX3KofjPQ4jjr6MV6sP7BhiEglz2jzmiWg tz_offset==UTC+03:00 per_page==10
  ```
##### Example Response
```
Status: 200 OK
```
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

## Production

[[TODO]]

## Development

If you would like to contribute, fork or simply demo this project, here's some info to help you run this locally.

You should have the following installed:

- [Python 3.7 or later](https://www.python.org/downloads/)
- [pyenv](https://github.com/pyenv/pyenv) (it's not needed, but makes life easier if you need to switch between Python versions)
- [Docker](https://docs.docker.com/get-docker/)
- [sqlcmd](https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility?view=sql-server-ver15)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- and an IDE would be helpful ([Visual Studio Code is nice](https://code.visualstudio.com/)).

### Project Structure

Monorepo with everything needed to run this project.

``` bash
/alembic    # Schema management  
/backend    # Flask app supporting blueprints for API and SPA dashboard
/docs       
/frontend   # SPA user interface  
/ingester   # Azure Functions for handling data loading
/tests
application.py        # Entry point into the backend app
docker-compose.yml    # Containers for Azurite and SQL Database 
Dockerfile.sqlserver  # Cstom SQL Server dockerfile to create init scripts
manage.py             # Entry point for alembic schema manager               
```

### Configuration

Configuration is modeled after [12-factor](https://12factor.net/) practices, all configurations are either declared directly in [settings.py](/backend/settings.py) or read from environment variables. On Azure, we'll use [App Service configurations](https://docs.microsoft.com/en-us/azure/app-service/configure-common) to provide the environment variables. Locally, during development we use [python-dotenv](https://github.com/theskumar/python-dotenv) to load a local `.env` file containing all the local configurations, including secrets. This local configuration file should not be checked into source control, so an [entry to have it ignored already exists in `.gitignore`](/.gitignore#L105)

To start, an [example `.env`](/.example-env) has been created at the base of this repo, just rename it to `.env` to use.

#### Setting Up OAuth Providers

The following steps are required for setting up OAuth.

##### Microsoft/Azure 

1. sign into the [Azure Portal](https://portal.azure.com), find `Azure Active Directory`
1. from `Azure Active directory` left menu, select `App registrations`
1. from `New registration` page, enter
   - `Name`: (e.g, myapp-api, myapp-api-development)
   - `Account Types`: choose in any organization (multitenant)
   - `Redirect`: http://localhost:5000/signin/azure/complete
1. Upon completion, select `go to resource`
1. from resource page left menu, select `Certificates & secrets`
   - click `+ New client secret` 
   - take note of client secret and key

##### GitHub

1. sign into [GitHub](https://github.com) and go to [Developer Settings](https://github.com/settings/apps) page
1. from left menu, select `OAuth Apps`
1. from `OAuth Apps` page, select top right `New OAuth App` button
1. on the `Register a new OAuth application` page, enter
   - `Application name`
   - `Homepage URL`
   - `Authorization callback URL`: http://localhost:5000/signin/github/complete
1. on new OAuth application page, 
   - click `Generate a new client secret` button
   - take note of `Client ID` and `Client secrets`

After obtaining the client key/id and secrets for `Azure` and `GitHub`, add them to the example `.env` you've renamed from earlier.

### Build and Run

Before building or running anything, let's install all the required dependencies for both Python and Node modules (our SPA is Svelte).

```bash
# terminal 1
cd <project-root>
echo '3.x.x' > .python-version             # assume you're using pyenv
python -m venv .venv                       # create virtual env
. .venv/bin/activate                       # activate the virtual env
(.venv) pip install -r requirements.txt    # install python dependencies

(.venv) npm install --prefix frontend      # install node dependencies
```

Great, we're ready to build and run our app. There are basically 4 different components to build/run: 

  * containers for Blob storage and SQL Database
  * frontend SPA
  * backend app (includes both API and SPA dashboard)
  * functions

Let's bring up the docker containers for our local SQL Database/Blob storage
```bash
# terminal 2 (new terminal)
cd <project-root>
docker-compose up
```

Let's create the schema for our application.
```bash
# terminal 1 (back to previous terminal)
(.venv) python manage.py db migrate
(.venv) python manage.py db upgrade
```

The frontend SPA can be built explicitly and run from the backend server or run in a separate development server (via webpack) if you are working on the frontend.

If just building the SPA for the backend app, then
```bash
# terminal 1 (still)
(.venv) npm run build --prefix frontend   # compile the SPA
# ^will create frontend/public/static/bundle.css, frontend/public/static/bundle.js 
```
the `bundle.css` and `bundle.js` will get [picked up by the `frontend.py`](/backend/frontend.py#L14).

If you plan on developing the frontend SPA, and want hot-reloading, you'll need to run it in it's own server (via webpack).

```bash
# terminal 3 (open up new terminal)
cd <project-root>
npm run dev --prefix frontend     # start server at localhost:8080 for the SPA 
# ^calls to the backend will be proxied
```
Check http://localhost:8080 for SPA frontend.

Finally to run the backend app

```bash
# terminal 1 (back to original terminal)
(.venv) python application.py
```

Check http://localhost:5000 to access the app. 

_Note: if you are running the frontend SPA (e.g, `npm run dev`) in addition to the backend, you should access the http://localhost:8080 for SPA and http://localhost:5000/api/... for API URLs._


[[TODO]] Functions

## Todos

- [ ] missing documentation on
  - [ ] channels endpoint
  - [ ] messages endpoint
  - [ ] production deployment process
  - [ ] development run Functions locally
- [ ] detailed how-to on
  - [ ] OAuth
  - [ ] SPA, Svelte
  - [ ] configurations

