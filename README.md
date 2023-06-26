# QueryCrafter

You can refer to this Medium [article](https://medium.com/p/97f60aa26708) for a detailed explanation of this project.


## How to run the agent?

To run this agent, you need to add the "development.yaml" file to the "config" folder. The structure of the file is as follows:

```yaml
env: development
secrets:
  api_tokens:
    generic: 'this is a test credential!'
  openai_api:
    token: ''
    organization: ''
  database:
    url: 'postgresql://postgres:postgres@localhost:5432/Adventureworks'
  slack:
    slack_bot_token: ''
    slack_signing_secret: ''
    slack_bot_user_id: ''
  metabase:
    metabase_url: 'http://localhost:3000'
    content_type: 'application/json'
    metabase_session: 'session for metabase'
    collection_parent: 'Collection parent: int'
    database_id: 'database id: int'
logging_level: DEBUG
```

The API tokens are not necessary for this assistant. However, you do need to have an OpenAI API token to access the GPT-4 model. Additionally, please provide the "Organization ID" for your organization. For database access, it is recommended to create a read-only user specifically for this assistant to ensure secure and limited access to the database.

For Slack access, you can follow this [tutorial](https://www.youtube.com/watch?v=3jFXRNn2Bu8&t=1510s&ab_channel=DaveEbbelaar), also this [page](https://docs.datalumina.io/3y3XPD66nBJaub/b/2808AFE6-41C8-46EF-A4AB-52A4B021993A/Part-1-%E2%80%94-Slack-Setup) is useful.

For Metabase configuration, there there are simple parts:

The metabase_url, is the URL for Metabase.
The Metabase session is a unique id for each instance of Metabase, you can follow this [tutorial](https://www.metabase.com/learn/administration/metabase-api#authenticate-your-requests-with-a-session-token) to get it.
The parent collection is a necessary component as it serves as the storage location for all the dashboards and subcollections created by the assistant. You can find the id of a collection in the URL.
The database ID refers to the specific database that Metabase will utilize for running queries. You can locate this ID in the URL within Metabase's admin panel.



With the "development.yaml" file ready, you can run the docker-compose to build and run the containers:
```
docker compose build --no-cache && docker compose up
```

To debug the agent in routers/slack.py, you have the option to modify the parameters. Set the 'verbose' parameter as 'True' to enable verbose mode, which is 'False' by default:

```python
agent = GeneralAgent(engine=engine, verbose=True)
```

Additionally, you have the option to use ngrok to establish a connection between your local environment and Slack. Ngrok provides a secure port forward functionality, allowing Slack to discover your local endpoint. To achieve this, you can utilize the following command:
```
ngrok http http://0.0.0.0:8080
```
Finally, you can use the QueryCrafter agent in your chat!!