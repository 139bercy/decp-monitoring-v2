FROM python:3.9-slim
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends --yes -y wget python3-venv python3-pip
RUN wget --output-document=decp.json https://www.data.gouv.fr/fr/datasets/r/16962018-5c31-4296-9454-5998585496d2 

