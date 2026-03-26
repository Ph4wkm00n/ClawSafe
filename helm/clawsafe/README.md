# ClawSafe Helm Chart

Deploy ClawSafe on Kubernetes.

## Quick Start

```bash
helm install clawsafe ./helm/clawsafe \
  --set secrets.apiKey=your-secret-key \
  --set secrets.jwtSecret=your-jwt-secret
```

## With Ingress

```bash
helm install clawsafe ./helm/clawsafe \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=clawsafe.example.com \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=Prefix \
  --set secrets.apiKey=your-secret-key
```

## With PostgreSQL

```bash
helm install clawsafe ./helm/clawsafe \
  --set config.dbType=postgresql \
  --set secrets.dbUrl=postgresql://user:pass@postgres:5432/clawsafe
```

## Configuration

See `values.yaml` for all configurable options.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `replicaCount` | `1` | Number of replicas |
| `backend.image.repository` | `clawsafe-backend` | Backend image |
| `frontend.image.repository` | `clawsafe-frontend` | Frontend image |
| `config.logLevel` | `INFO` | Log level |
| `config.scanInterval` | `3600` | Scan interval (seconds) |
| `config.demoMode` | `false` | Enable demo data |
| `config.dbType` | `sqlite` | Database type |
| `config.trivyEnabled` | `false` | Enable CVE scanning |
| `secrets.apiKey` | `""` | API key for write endpoints |
| `secrets.jwtSecret` | `""` | JWT signing secret |
| `ingress.enabled` | `false` | Enable Ingress |
| `persistence.enabled` | `true` | Enable persistent storage |
| `persistence.size` | `5Gi` | Storage size |
| `autoscaling.enabled` | `false` | Enable HPA |
