

```
docker build -t consumergroup-monitor .
```

```
docker run -itd --restart always --name consumergroup-monitor consumergroup-monitor:latest
```


# Trigger Update Spark Application ConsumerGroupID

```
curl -X POST \
     -F token={token} \
     -F ref={branch} \
     https://gitlabhost/api/v4/projects/482/trigger/pipeline
```
