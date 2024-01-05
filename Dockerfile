FROM python:3.12
WORKDIR /mood-of-the-day
COPY . .
RUN python -mpip install -U '.'
ENTRYPOINT ["python", "src"]
