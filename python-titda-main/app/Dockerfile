FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD [ "app.py"]