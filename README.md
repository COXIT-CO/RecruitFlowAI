# CVScanAI
AI Driven CV Validator


## Deployment
1. Create in base folder `.env` file and specify:
   - `SLACK_ACCESS_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `SLACK_BOT_DATA_PATH`
2. Build docker image `docker build -t cv_scan_ai_image .`
3. Run container `docker run -d --name cv_scan_ai_cont  -p 3000:3000 --restart=always cv_scan_ai_image`