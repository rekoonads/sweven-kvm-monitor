# KVM Monitor Service - Railway Deployment

System monitoring service for Sweven Games infrastructure. Collects metrics from servers and sends to InfluxDB.

## Technology Stack
- **Language**: Python 3
- **Monitoring**: InfluxDB Client
- **Scheduler**: schedule library
- **Metrics**: psutil, libvirt (optional)

## Important Note

**KVM/libvirt dependency**: This service includes KVM monitoring which requires `libvirt-python`. Since Railway runs in containerized environments without KVM access, the KVM monitoring module will be automatically disabled. The service will still collect other system metrics (CPU, memory, disk, network).

## Railway Deployment Steps

### 1. Create Railway Project
```bash
cd "d:\cloud gaming\backend-services\kvm-monitor"
railway login
railway init
```

### 2. Set Environment Variables
```bash
railway variables set INFLUX_URL=https://influxdb.swevengames.in
railway variables set INFLUX_TOKEN=your_influxdb_token
railway variables set INFLUX_ORG=sweven-games
railway variables set INFLUX_BUCKET=monitoring
railway variables set MONITORING_INTERVAL=60
railway variables set LOG_LEVEL=INFO
```

### 3. Deploy
```bash
railway up
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `INFLUX_URL` | InfluxDB server URL | - | Yes |
| `INFLUX_TOKEN` | InfluxDB authentication token | - | Yes |
| `INFLUX_ORG` | InfluxDB organization name | - | Yes |
| `INFLUX_BUCKET` | InfluxDB bucket for metrics | - | Yes |
| `MONITORING_INTERVAL` | Collection interval (seconds) | 60 | No |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO | No |

## Monitored Metrics

### System Metrics (Available on Railway)
- **CPU**: Usage percentage, load average
- **Memory**: Total, used, available, percentage
- **Disk**: Total, used, free, percentage
- **Network**: Bytes sent/received, packets

### KVM Metrics (Disabled on Railway)
- **VM Status**: Running, stopped VMs
- **VM Resources**: CPU time, memory usage
- **VM Network**: Interface statistics

## Configuration

Module configuration is stored in `config/modules_config.json`. Available modules:
- `system_monitor` - System resource monitoring
- `network_monitor` - Network statistics
- `disk_monitor` - Disk usage
- `kvm_monitor` - KVM/libvirt (auto-disabled without libvirt)

## Deployment Considerations

1. **No KVM Access**: Railway doesn't provide KVM/libvirt access, so VM monitoring will be disabled
2. **Resource Monitoring**: System metrics (CPU, RAM, network) will still work
3. **Persistent Connection**: Maintains connection to InfluxDB for metric storage
4. **Restart Policy**: Automatically restarts on failure

## InfluxDB Setup

You'll need a separate InfluxDB instance. Options:
1. Deploy InfluxDB on Railway as a separate service
2. Use InfluxDB Cloud (https://cloud2.influxdata.com/)
3. Self-host InfluxDB elsewhere

## Alternative Deployment

For full KVM monitoring capabilities, deploy this service on your actual gaming servers (not Railway):
```bash
# On your gaming server with KVM
cd /opt/sweven-games
git clone <your-repo>
cd kvm-monitor
pip install -r requirements.txt
python main.py
```

Or use the provided systemd service:
```bash
sudo ./install.sh
sudo systemctl start kvm-monitor
sudo systemctl enable kvm-monitor
```
