FROM python:3

COPY . /
# RUN make install
RUN pip install flask
EXPOSE 5000

CMD ["python3","minesweeper.py","--web"]


# docker build -t minesweeper .
# docker run --rm -p 5000:5000 minesweeper
# 1205  docker commit hungry_pascal tibblue/graphdb_prc:v3.0
# 1207  docker push tibblue/graphdb_prc:v3.0
# 1213  docker run -p 7200:7200 tibblue/graphdb_prc:v3.0
# 1245  docker image rm -f tibblue/graphdb_prc:v3.0
