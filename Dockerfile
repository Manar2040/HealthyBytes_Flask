FROM python:latest
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["flask","run","--host=0.0.0.0","--port=5000"]
