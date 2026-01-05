FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /django_qrcode
RUN apt-get update
RUN pip3 install opencv-python-headless==4.5.3.56
RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
COPY requirnments.txt requirnments.txt
RUN pip3 install -r requirnments.txt
