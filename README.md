# slids
Simple and Light IDS

# prereq's
Running this kajigger on Raspberry Pi 5.

```
mkdir /mnt/mytmpfs
apt -y install suricata suricata-update
```
- copy surricata.yaml to /etc/suricata
- mount tmpfs partition
- install tzsp2pcap
- (install and) start tzsp2pcap streaming server
```
wget https://github.com/scavara/tzsp2pcap/releases/download/1.0.0-1/tzsp2pcap_1.0.0-1_arm64.deb
dpkg -i tzsp2pcap_1.0.0-1_arm64.deb
nohup tzsp2pcap -f -o /mnt/mytmpfs/capture.pcap -G 120 &
```
- (configure and) start Packet Sniffer on mikrotik router

setup service
```
cp mnt/mytmpfs/log_cleaner.py /mnt/mytmpfs/
cp mikrotik2pcap.* /etc/systemd/system
systemctl daemon-reload
systemctl start mikrotik2pcap.timer
```
- import alerts and dashboard in grafana (cloud) from grafana-cloud dir

```
+---------------------+
| Mikrotik Router     |------------------------------------+
| Packet Sniffer      |                                    |
|                     |                                    |
+---------------------+                                    |
                                                           | 
                                                           |
                                                  +--------v------------+
                                                  |                     |
                                                  | tzsp2pcap           |
                                                  | streaming server    |
                                                  | (port 37008)        |
                                                  |                     |
                                                  +--------+------------+
                                                           | tzsp2pcap
                                                           | (output)
                                                           |
                                                  +--------v------------+
                                                  |                     |
                                                  |  capture.pcap       |
                                                  |                     |
                                                  +--------+------------+
                              +--------------------------------------------+
                              |        +-------------------------+         |
                              |        |   systemd service/timer |         |
                              |        +-----------+-------------+         |
                              |                    | (every minute)        |
                              |                    |                       |
                              |                    | runs:                 |
                              |                    |                       |
                              |      +-------------v------------+          |
                              |      |                          |          |
                              |      |     Suricata service     |          |
                              |      |  (analyzes capture.pcap  |          |
                              |      |   outputs to eve.json)   |          |
                              |      |                          |          |
                              |      +-------------+------------+          |
                              |                    |                       |
                              |      +-------------v-------------+         |
                              |      |                           |         |
                              |      |    eve.json               |         |
                              |      |                           |         |
                              |      |                           |         |
                              |      |                           |         |
                              |      +-------------+-------------+         |
                              |                    |                       |
                              |                    | (remove log entries   |
                              |                    |  older than 2 mins)   |
                              +--------------------------------------------+
                                                   ^
                                                   | (scrape)
                                                   |
                                         +---------+------------+
                                         |                      |
                                         |      Promtail        |
                                         |                      |
                                         +---------+------------+
                                                   |
                                                   | (send logs)
                                                   |
                                         +---------v-------------+
                                         |                       |
                                         |   Loki (Grafana       |
                                         |         Cloud)        |
                                         |                       |
                                         +---------+-------------+
                                                   ^
                                                   | (query logs)
                                                   |
                                        +----------+-------------+
                                        |                        |
                                        |  Grafana Panel/Alert   |
                                        |  (data source: Loki)   |
                                        |                        |
                                        +------------------------+

```
# thanks and creds
- https://github.com/thefloweringash/tzsp2pcap
- https://suricata.io/
- https://grafana.com/grafana/dashboards/22247-suricata-logs-json/
- https://grafana.com/products/cloud/
