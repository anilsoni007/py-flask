FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY panda_app.py /app

EXPOSE 5000

# Set the environment variable for Flask to run
ENV FLASK_APP=panda_app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]