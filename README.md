# Python Backdoor

There are many ways to access remote computers. It can be over SSH, to use reverse shell, to use Python Paramiko etc.

In this project, I have built a backdoor over HTTPS, which is useful when SSH is not installed on the remote machine.

This kind of backdoor, could be interesting to use in Docker containers too, so therefore, I have a run_script.sh file instead of initd or systemd files.

## Installation and Configuration

To install, run

```bash
sudo install.sh
```

then edit `/opt/backdoor/config/.env` with your desired values

```bash
SECRET_KEY=JamesBond007
MAX_DELAY=5000
```

where MAX_DELAY is the max delay in milliseconds in your HTTPS request to the backdoor.

