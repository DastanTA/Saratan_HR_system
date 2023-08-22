FROM python:3.10
EXPOSE 5000
WORKDIR /app

# Set DEBIAN_FRONTEND to noninteractive to avoid prompts
#ENV DEBIAN_FRONTEND noninteractive

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
