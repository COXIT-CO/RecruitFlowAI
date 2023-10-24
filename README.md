# RecruitFlowAI

RecruitFlowAI is a Slack bot with OpenAI integration aimed to assist COXIT's recruiters during the entire recruitment pipeline.

## Table of Contents

- [RecruitFlowAI](#recruitflowai)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Actively Developing Functionality for Release 0.1.0.](#actively-developing-functionality-for-release-010)
  - [Slack Bot](#slack-bot)
    - [Setting Up the Bot](#setting-up-the-bot)
    - [Deployment](#deployment)
    - [Commands](#commands)
  - [Project Structure](#project-structure)
  - [RecruitFlowAI Bot Demo](#recruitflowai-bot-demo)

## Project Description

At the current stage the project is proof of concept. It utilises [ChatCraft.org](https://chatcraft.org/) to enhance the user experience and chatting with OpenAI. This approach was choosen to speed up prompt engineering and experimenting with OpenAI - the bot is already integrated in our recruitment process and we are activly using it!

The typical recruitment process in COXIT involves creating job descriptions for job sites and social media posts, analyzing a batch of resumes sent by candidates or found in the internal resume database, matching those resumes, screening the candidates, reformating and summarization of feedbacks, and more.

RecruitFlowAI should automate this process to ensure fast and high-quality of routine checks and analysis. Integrated OpenAI assistant will check grammar and spelling mistakes in resumes and job descriptions, helping to identify errors that may not be easily noticed with other grammar validator like Gramarly. It will do the analysis of resumes, summurisations of reports and feedbacks. It will also connect to the internal database to match relevant resumes to the job requirements helping the recruiter to prioritize screenings with candidates.

For more details checkout the [project Notion](https://cotton-radar-ab3.notion.site/CVScanAI-25ca5c0e61fd4ad284796443dd258c3a).

## Actively Developing Functionality for Release 0.1.0.

- Slack Bot as UI.
- PDF formatted resume scanning for mistakes.
- Matching resumes to job description and prioritizing candidates with detailed summary for each.
- Search of candidates in internal database based on job requirements.
- AI assistant integrated into Slack Bot.

## Slack Bot

### Setting Up the Bot

1. Go to [api.slack.com/apps](https://api.slack.com/apps), log into your workspace and click on Create an app(you can add the existing manifest or create App from Scratch)
2. Generate all required api tokens and secrets: access token, signing secret, config token...(check instructions below)
3. Use these data and bot app id to populate env variables mentioned below.

### Deployment

1. Create in base folder `.env` file and specify:

   - `SLACK_ACCESS_TOKEN` - Bot User OAuth Token.
   - `SLACK_SIGNING_SECRET` - Signing Secret from the App credentials section.
   - `SLACK_CONFIG_DATA_DIR` - the path to the directory that contains `manifest.json` and `chatcraft_templates.json` (optional for docker run).
   - `SLACK_BOT_APP_ID` - App ID from the App credentials section.
   - `SLACK_APP_CONFIG_TOKEN` - Access Token from App Configuration Tokens(**Your Apps** section). Used to create and configure Slack apps using App Manifest APIs: https://api.slack.com/authentication/config-tokens
   - `SLACK_REFRESH_TOKEN` - refresh token for app config token rotation if the token was refreshed at least once with request/api. Obtain it from **Your Apps**, same as the app config token: https://api.slack.com/apps.
   - `SLACK_ACCESS_TOKEN` - Bot User OAuth Token. Install App to Workspace and copy it from the `Install App->OAuth Tokens for Your Workspace` section
   - `OPENAI_API_KEY` - generate this key in your OpenAI account: https://platform.openai.com/account/api-keys.

   #### You can find additional information about tokens [here](https://api.slack.com/authentication/token-types)

2. Run the bot & Loki Grafana logging services with `docker compose up` while being in the base folder.

   _Logs are accessible to view with Grafana at localhost:3200 by default after all the services started_

### Commands

- `/generate_job_description` - pass all you know about the job requirements, client and interview procedure to generate job description.
- `/create_social_media_post` - pass job description and generate post for social media
- `/match_resumes` - pass job requirements and link to resumes to know which of candidates are more suitable
- `/scan_resume` - pass link to PDF formatted resume and get lost of mistakes found, and suggested corrections

Note: all the commands above can take Chatcraft url or hint text `Hint: ...` as text parameters, it will update the configuration for all users

- `/save_resume <link>` - add resume to internal S3 storage and return the link
- `/search_db` - pass job description and receive list of candidates from internal database
- `/assistant` - chat with OpenAI from recruiter persona

Messaging with AI assistant - just ask any question in RecruitFlowAI home app and receive response in the thread! Conversation can be proceeded in the same chat and resumed any tiem later.

Commands to be designed and added later:

- `/brand_resume`
- `/compose_feedback`
- `/generate_job_report`

## Project Structure

The project follows the following directory structure:

```
.
├── Dockerfile
├── README.md
├── recruit_flow_ai
├── requirements.txt
├── setup.py
├── slack_bot
└── version.py
```

- `Dockerfile` - docker file to start Slack Bot
- `README.md` - the main documentation file for the project.
- `recruit_flow_ai` - OpenAI integration module
- `requirements.txt` - test dependencies common for all modules.
- `setup.py` - currently setup to be used for CI purposes only.
- `slack_bot` - RecruitFlowAI Bot
- `version.py` - project's main versioning file.

## RecruitFlowAI Bot Demo

![RecruitFlowAI Bot Home](https://github.com/COXIT-CO/RecruitFlowAI/blob/dev/media/RecruitFlowAI_Home.png)

![About](https://github.com/COXIT-CO/RecruitFlowAI/blob/dev/media/RecruitFlowAI_Commands.png)
![OpenAI Chat Thread Part 1](https://github.com/COXIT-CO/RecruitFlowAI/blob/dev/media/RecruitFlowAI_ChatThread_1.png)
![OpenAI Chat Thread Part 1](https://github.com/COXIT-CO/RecruitFlowAI/blob/dev/media/RecruitFlowAI_ChatThread_2.png)
