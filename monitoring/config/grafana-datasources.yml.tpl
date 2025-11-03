apiVersion: 1

datasources:
  - name: Gaming Forum Metrics
    type: prometheus
    access: proxy
    url: https://${prometheus_fqdn}
    isDefault: false
    editable: true
    jsonData:
      httpMethod: GET
      timeInterval: 15s
    uid: prometheus-gaming-forum
  
  - name: Gaming Forum DB
    type: postgres
    access: proxy
    url: ${postgres_url}
    database: forum_db
    user: ${postgres_user}
    secureJsonData:
      password: '${postgres_password}'
    jsonData:
      sslmode: 'require'
      postgresVersion: 1600
    isDefault: true
    editable: true
    uid: postgres-gaming-forum
