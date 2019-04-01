FROM ubuntu:18.04
MAINTAINER roy@moore.co.il

# Install packages
RUN apt update && apt install nginx mongodb python3 python3-pip -y

# Copy code
COPY . /code
WORKDIR /code

# Update nginx conf
COPY conf/print_similar.conf /etc/nginx/conf.d/print_similar.conf
# Remove nginx default conf
RUN echo > /etc/nginx/sites-available/default

# Install requirements
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 8000

CMD /etc/init.d/nginx start && ./run_server.sh;
