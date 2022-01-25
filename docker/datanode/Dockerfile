#CMD ["sleep 30", "|", "hdfs", "dfs", "-mkdir", "/FilmPosters", '|', "hdfs", "dfs", "-copyFromLocal", "/home/*.jpg", "/FilmPosters", '|', "/run.sh"]
FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

MAINTAINER Ivan Ermilov <ivan.s.ermilov@gmail.com>

HEALTHCHECK CMD curl -f http://localhost:9864/ || exit 1

ENV HDFS_CONF_dfs_datanode_data_dir=file:///hadoop/dfs/data
RUN mkdir -p /hadoop/dfs/data
RUN apt-get update && apt-get install -y \
    python3.6 \
    python3-pip
RUN pip3 install flask
VOLUME /hadoop/dfs/data


ADD datanode/run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 9864

CMD ["/run.sh"]