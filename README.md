# RecruitFlowAI
RecruitFlowAI is a Slack bot with OpenAI integration aimed to assist COXIT's recruiters during the entire recruitment pipeline.

## Table of Contents
- [RecruitFlowAI](#recruitflowai)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Actively Developing Functionality for Release 0.1.0.](#actively-developing-functionality-for-release-010)
  - [Slack Bot](#slack-bot)
    - [Deployment](#deployment)
    - [Comamnds](#comamnds)
  - [AI CV Parser](#ai-cv-parser)
    - [Usage Example](#usage-example)
  - [Project Structure](#project-structure)


## Project Description
At the current stage the project is proof of concept. It utilyses [ChatCraft.org](https://chatcraft.org/) to enhance the user experience and chatting with OpenAI. This approach was choosen to speed up prompt engineering and experimenting with OpenAI - the bot is already integrated in our recruitment process and we are activly using it!

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

### Deployment
1. Create in base folder `.env` file and specify:
   - `SLACK_ACCESS_TOKEN` - Bot User OAuth Token
   - `SLACK_SIGNING_SECRET` - Signing Secret from the App credentials section 
   - `SLACK_CONFIG_DATA_DIR` - the path to the directory that contains `manifest.json` and `chatcraft_templates.json` (optional for docker run)
   - `SLACK_BOT_APP_ID` - App ID from the App credentials section 
   - `SLACK_APP_CONFIG_TOKEN` - needed to run the bot using ngrok. It expires every 12 hours, do not forget to update ([reference](https://api.slack.com/authentication/config-tokens)). You will need to have ngrok configured -  check `.ngrok2/ngrok.ym` in you home dir, it should contain `authtoken` and `version` set to `2`. Read more details on https://dashboard.ngrok.com/get-started/setup.

2. Build docker image `docker build -t recruit_flow_bot_image .`
3. Run container `docker run -d --name recruit_flow_bot_cont  -p 3000:3000 --restart=always recruit_flow_bot_image`


### Comamnds
- `/generate_job_description` - pass all you know about the job requirements, client and interview procedure to generate job description.
- `/create_social_media_post` - pass job description and generate post for social media
- `/match_resumes` - pass job requirements and link to resumes to know which of candidates are more suitable
- `/scan_resume` - pass link to PDF formatted resume and get lost of mistakes found, and suggested corrections

Note: all the commands above can take chatcraft url or hint text `Hint: ...` as text parameters, it will update the configuration for all users

- `/save_resume <link>` - add resume to internal DB
- `/search_db` - pass job description and receive list of candidates from internal database
- `/assistant` - chat with OpenAI from recruiter persona

Commands to be designed and added later:
- `/brand_resume`
- `/compose_feedback`
- `/generate_job_report`

## AI CV Parser
Python package that provides the functionality to parse the CVs in the PDF format and extract the next information using GPT-4 model:
- email
- full_name
- summary
- list of mentioned skills 
- education
- experience

### Usage Example
```
from ai_cv_parser import parse_resume

with open('cv.pdf') as file:
   resume_model = parse_resume(file)

```


## Project Structure
The project follows the following directory structure:
```
.
├── Dockerfile
├── README.md
├── ai_assistant
│   └── openai
├── requirements.txt
├── setup.py
├── slack_bot
└── version.py
```

- `Dockerfile` - docker file to start Slack Bot
- `README.md` - the main documentation file for the project.
- `ai_assistant/openai` - openai integration module (api and logic to be imported in other modules)
- `requirements.txt` - test dependencies common for all modules.
- `setup.py`  - currently setup to be used for CI purposes only.
- `slack_bot` - RecruitFlowAI Bot  
- `version.py` - project's main versioning file.
