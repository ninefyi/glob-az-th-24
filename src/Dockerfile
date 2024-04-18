FROM python:3.10-slim

WORKDIR /workspace

ADD requirements.txt chat_bot.py secret.py /workspace/

RUN pip install -r /workspace/requirements.txt

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "/workspace/chat_bot.py"]