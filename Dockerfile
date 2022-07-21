FROM ubuntu:16.04
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends --yes -y wget python3-pip
RUN pip install pandas datetime
