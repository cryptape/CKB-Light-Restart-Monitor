# CKB-Light-Restart-Monitor

CKB-Light-Restart-Monitor is a utility that simplifies the process of downloading, monitoring, and periodically restarting the CKB-Light-Client.

## Installation

1. Download the CKB-Light-Client:

   ```shell
   git clone https://github.com/nervosnetwork/ckb-light-client.git
   cd ckb-light-client
   git checkout develop
   cargo build --release
   ```

2. Monitor the CKB-Light-Client:

   ```shell
   pip install prometheus_client
   python monit.py
   ```

3. Schedule automatic restart every 3 days using crontab:

   ```shell
   0 0 */3 * * sudo nohup bash /home/ckb/gp/CKB-Light-Restart-Monitor/restart.sh &
   ```



