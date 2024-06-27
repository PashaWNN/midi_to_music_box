FROM python:3.10-slim

RUN apt-get update

RUN apt-get -y full-upgrade

RUN apt-get install -y --no-install-recommends \
	libcairo2 libdouble-conversion3 libxml2 lib3mf1 libzip4 libharfbuzz0b \
	libboost-thread1.74.0 libboost-program-options1.74.0 libboost-filesystem1.74.0 \
	libboost-regex1.74.0 libmpfr6 libqscintilla2-qt5-15 \
	libqt5multimedia5 libqt5concurrent5 libtbb12 libglu1-mesa \
	libglew2.2 xvfb xauth openscad

RUN apt-get clean


WORKDIR /usr/src/app
RUN mkdir /gradiofiles
RUN pip install --no-cache-dir gradio
COPY . .
RUN pip install -r requirements.txt
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_TEMP_DIR="/gradiofiles"

CMD ["python", "app.py"]
