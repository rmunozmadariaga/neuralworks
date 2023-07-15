FROM python:3.9

# Copy local code to the container image.
ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME

COPY . ./

# Install dependencies.
RUN pip install --no-cache-dir --upgrade -r $APP_HOME/requirements.txt

EXPOSE $PORT


