mapping ={
  "mappings": {
    "properties": {
      "@timestamp": {"type": "date"},
      "error": {"type": "boolean"},
      "message": { "type": "text"},
      "request": {
        "properties": {
          "host": {"type": "text"},
          "url": {"type": "text"}
        }
      },
      "status": {
        "properties": {
          "cluster": {"type": "text"},
          "complete": {"type": "long"},
          "group": {"type": "text"},
          "appname": {"type": "text"},
          "maxlag": {
            "properties": {
              "client_id": {"type": "text"},
              "complete": {"type": "long" },
              "current_lag": {"type": "long" },
              "end": {
                "properties": {
                  "lag": {"type": "long" },
                  "observedAt": {"type": "date"},
                  "offset": {"type": "long"},
                  "timestamp": {"type": "date"}
                }
              },
              "owner": {"type": "text"},
              "partition": {"type": "long"},
              "start": {
                "properties": {
                  "lag": {"type": "long" },
                  "observedAt": {"type": "date"},
                  "offset": {"type": "long" },
                  "timestamp": {"type": "date" }
                }
              },
              "status": {"type": "text"},
              "topic": { "type": "text" }
            }
          },
      "partition_count": {"type": "long" },
      "status": {"type": "text"},
      "totallag": { "type": "long"}}
      }
    }
  }
}