FROM python:3.9

WORKDIR /cv_scan_ai

COPY ./requirements.txt /cv_scan_ai/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /cv_scan_ai/requirements.txt

COPY ./slack_bot /cv_scan_ai/slack_bot

COPY ./slack_bot/data /cv_scan_ai/data

COPY ./.env /cv_scan_ai/.env

CMD ["uvicorn", "slack_bot.main:app", "--host", "0.0.0.0", "--port", "3000", "--proxy-headers"]