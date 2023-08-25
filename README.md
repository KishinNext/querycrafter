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
    url: 'postgresql://postgres:postgres@host.docker.internal:5432/Adventureworks'
  slack:
    slack_bot_token: ''
    slack_signing_secret: ''
    slack_bot_user_id: ''
  metabase:
    metabase_url: 'http://host.docker.internal:3000'
    content_type: 'application/json'
    metabase_session: 'session for metabase'
    collection_parent: 'Collection parent: int'
    database_id: 'database id: int'
logging_level: DEBUG
```
> Please note that the database URL and metabase_url correspond to the address of your desired database connection and your Metabase instance, respectively. The URL provided above is for the AdventureWorks database and a Metabase instance, both running locally through Docker. You're welcome to adjust it to reflect your own database URL
The API tokens are not necessary for this assistant. However, you do need to have an OpenAI API token to access the GPT-4 model. Additionally, please provide the "Organization ID" for your organization. For database access, it is recommended to create a read-only user specifically for this assistant to ensure secure and limited access to the database.

### Slack

To set up the Slack integration, you'll need to create a Slack app. For guidance on Slack configuration, please refer to this [tutorial](https://www.youtube.com/watch?v=3jFXRNn2Bu8&t=1510s&ab_channel=DaveEbbelaar).
Additionally, this documentation page is a valuable resource for obtaining the **Slack_Bot_id** and configuring the app [page](https://docs.datalumina.io/3y3XPD66nBJaub/b/2808AFE6-41C8-46EF-A4AB-52A4B021993A/Part-1-%E2%80%94-Slack-Setup).


 
### Database

Querycrafter is compatible with Postgres databases. You have the option to either utilize your own database or employ the one showcased in this demo.

For this demonstration, I've implemented the AdventureWorks database for PostgreSQL. You can download it [here](https://github.com/lorint/AdventureWorks-for-Postgres)

Please ensure you've set this up before proceeding to the subsequent steps.

### Metabase
For Metabase configuration, there are simple parts:

First get the latest image of Metabase:
```
docker pull metabase/metabase:v0.46.4
```

Then run the image:
```
docker run -d -p 3000:3000 --name metabase metabase/metabase:v0.46.4
```

Connect your database to Metabase (if you use the AdventureWorks database locally here is the configuration):

![img.png](assets/database_config.png)


Get the url of Metabase:


The Metabase session is a unique id for each instance of Metabase, you can follow this [tutorial](https://www.metabase.com/learn/administration/metabase-api#authenticate-your-requests-with-a-session-token) to get it.
The parent collection is a necessary component as it serves as the storage location for all the dashboards and subcollections created by the assistant. You can find the id of a collection in the URL. For example, the id of the "gg" collection is 2.

![img.png](assets/collection_id.png)

The database ID refers to the specific database that Metabase will utilize for running queries. You can locate this ID in the URL within Metabase's admin panel. For example, the id of the "Adventureworks" database is 2.

![img.png](assets/database_id.png)

### Docker

With the "development.yaml" file ready, you can run the docker-compose to build and run the containers:
```
docker compose build --no-cache && docker compose up
```

To debug the agent in routers/slack.py, you have the option to modify the parameters. Set the 'verbose' parameter as 'True' to enable verbose mode, which is 'False' by default:

```python
agent = GeneralAgent(engine=engine, verbose=True)
```

### Ngrok
Additionally, you can use ngrok to establish a connection between your local environment and Slack. Ngrok provides a secure port forward functionality, allowing Slack to discover your local endpoint. To achieve this, you can utilize the following command:
```
ngrok http http://0.0.0.0:8080
```
Copy the forwarding URL and paste it in the "Event Subscriptions" section of your Slack app. You must also add "/slack/events" to the end of the URL to ensure that Slack can access the correct endpoint.
```
https://<your_ngrok_forwarding_url>/slack/events
```

Remember that you have to add your Slack app to your workspace before you can use it. 
You can follow this [tutorial](https://www.youtube.com/watch?v=dKSiV0s0Jkg) to add your Slack app to your workspace.


Finally, you can use the QueryCrafter agent in your chat!!

- Some examples :) :

![img.png](assets/questions_to_querycrafter.png)

- Here is the result:

![img.png](assets/dashboard.png)