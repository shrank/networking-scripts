
# Dockerfile for building nw-search.
#
# @see https://github.com/shrank/networking-scripts
#
# Version 0.3
#


# pull base image
FROM alpine:3.9.3

# Group ID for data files		
ENV DATA_GID 1
ENV SVNREPO /data/repo
ENV SVNDB_FRONTEND YES

MAINTAINER shrank <info@murxs.ch>
# Port for search frontend
EXPOSE 80/tcp

RUN apk add --no-cache ansible nmap py3-requests subversion python3 gcc libc-dev python3-dev make && ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install uvicorn starlette aiofiles

# add search
ADD SVN-DB/backend/ /srv/SVN-DB/
RUN cd /srv/SVN-DB/ && make

# ansible config and modules
COPY ansible.cfg /etc/ansible/ansible.cfg
ADD src/find_aps_filter.py /usr/share/ansible/plugins/filter/
RUN mkdir -p /usr/share/my_modules/ && wget -O /usr/share/my_modules/netonix_command.py https://raw.githubusercontent.com/shrank/python_netonix_api/master/ansible/netonix_command.py
RUN wget -O /usr/lib/python3.6/site-packages/netonix_api.py https://raw.githubusercontent.com/shrank/python_netonix_api/master/netonix_api.py

VOLUME ["/data"]
COPY ansible_dirs/ /distdata/
RUN chmod g+w  -R /distdata

# add entry script
ADD entry.sh /
RUN chmod a+x /entry.sh
CMD ["sh","/entry.sh"]
