FROM python:3.9-slim
RUN apt-get update && apt-get upgrade
RUN wget --output-document=data/decp.json https://www.data.gouv.fr/fr/datasets/r/16962018-5c31-4296-9454-5998585496d2

