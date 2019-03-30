FROM ubuntu:18.04
MAINTAINER roy@moore.co.il

# Install Nginx
RUN apt update && apt install nginx python3 python3-pip -y

# Copy code
COPY . /code
WORKDIR /code
# Install requirements
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 8000

CMD ./run_server.sh
