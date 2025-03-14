FROM python:3.13.1 

RUN apt-get update -y && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN reflex init

ARG SITE_NAME
ENV SITE_NAME=${SITE_NAME}

ARG N_ELEMENTS
ENV N_ELEMENTS=${N_ELEMENTS}

RUN reflex export --frontend-only --no-zip

# Needed until Reflex properly passes SIGTERM on backend.
STOPSIGNAL SIGKILL

CMD reflex run --env prod --backend-only
