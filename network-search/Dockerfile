# Dockerfile for building nw-search.
#
# @see https://
#
# Version 0.1
#


# pull base image
FROM alpine:3.9.3

MAINTAINER shrank <info@murxs.ch>
# Port for search frontend
EXPOSE 80/tcp
# Group ID for data files		
ENV DATA_GID 1


RUN apk add --no-cache ansible nmap subversion py3-requests && ln -s /usr/bin/python3 /usr/bin/python

# ansible config and modules
COPY ansible.cfg /etc/ansible/ansible.cfg
ADD src/find_aps_filter.py /usr/share/ansible/plugins/filter/
RUN mkdir -p /usr/share/my_modules/ && wget -O /usr/share/my_modules/netonix_command.py https://raw.githubusercontent.com/shrank/python_netonix_api/master/ansible/netonix_command.py
RUN wget -O /usr/lib/python3.6/site-packages/netonix_api.py https://raw.githubusercontent.com/shrank/python_netonix_api/master/netonix_api.py

# add search frontend
COPY src/server.py /app/server.py

# add entry script
ADD entry.sh /
RUN chmod a+x /entry.sh
CMD ["/entry.sh"]


VOLUME ["/data"]
COPY ansible_dirs/ /distdata/
RUN chmod g+w  -R /distdata
