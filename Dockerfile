#run with docker build -t wordlebot .
FROM ubuntu:22.04

ENV LC_ALL="C.UTF-8"
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update
RUN apt-get install -y python3 python3-pip 
RUN pip install python-dotenv discord.py
WORKDIR /bot
COPY bot.py .env cascada.txt paroles.txt /bot/
ENTRYPOINT ["python3", "bot.py"]