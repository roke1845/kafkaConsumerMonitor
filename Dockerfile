FROM python:3.7.4-alpine
ENV PYTHONUNBUFFERD=1
ENV TZ=Asia/Taipei
RUN echo "TZ='Asia/Taipei'; export TZ" >> ~/.profile

RUN mkdir -p project
WORKDIR /project
COPY . ./
RUN pip install -r requirements.txt

CMD ["python", "getGroupAndAlarmDriver.py"]