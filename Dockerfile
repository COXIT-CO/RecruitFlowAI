FROM python:3.9

WORKDIR /recruit_flow_ai

COPY ./requirements.txt /recruit_flow_ai/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /recruit_flow_ai/requirements.txt

COPY ./recruit_flow_ai /recruit_flow_ai/recruit_flow_ai

COPY ./slack_bot /recruit_flow_ai/slack_bot

COPY ./slack_bot/config_data /recruit_flow_ai/config_data

COPY ./.env /recruit_flow_ai/.env

CMD ["uvicorn", "slack_bot.main:fast_app", "--host", "0.0.0.0", "--port", "3000", "--proxy-headers"]