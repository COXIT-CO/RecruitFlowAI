FROM python:3.9

WORKDIR /recruit_flow_bot

COPY ./requirements.txt /recruit_flow_bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /recruit_flow_bot/requirements.txt

COPY ./slack_bot /recruit_flow_bot/slack_bot

COPY ./slack_bot/config_data /recruit_flow_bot/config_data

COPY ./.env /recruit_flow_bot/.env

CMD ["uvicorn", "slack_bot.main:app", "--host", "0.0.0.0", "--port", "3000", "--proxy-headers"]