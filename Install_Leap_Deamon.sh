#/bin/bash

# set -e
# todo: finalize this

dpkg --install LEAP/Leap-2.3.1+31549-x64.deb || echo "Ignore fail due to unmaintained package"
apt-get install -f
cp LEAP/leapd.service /lib/systemd/system/leapd.service
# you might need to ln -s /lib/systemd/system/leapd.service /etc/systemd/system/leapd.service
systemctl enable leapd
systemctl start leapd
