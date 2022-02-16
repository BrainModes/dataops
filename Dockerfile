FROM python:3.7-buster

ARG pip_username
ARG pip_password

WORKDIR /usr/src/app
ENV TZ=America/Toronto

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && apt-get update && \
apt-get install -y vim-tiny less && ln -s /usr/bin/vim.tiny /usr/bin/vim && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && chmod +x gunicorn_starter.sh
RUN PIP_USERNAME=$pip_username PIP_PASSWORD=$pip_password pip install --no-cache-dir -r internal_requirements.txt

CMD ["./gunicorn_starter.sh"]
