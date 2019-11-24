apt install vim
pip3 install ds4drv
echo "daemon=true" > /etc/ds4drv.conf


apt install build-essential cmake
cd ~
mkdir -p /opt/intel/openvino
wget https://download.01.org/opencv/2019/openvinotoolkit/R3/l_openvino_toolkit_runtime_raspbian_p_2019.3.334.tgz
tar -xf  l_openvino_toolkit_runtime_raspbian_p_2019.3.334.tgz --strip 1 -C /opt/intel/openvino
echo "source /opt/intel/openvino/bin/setupvars.sh" >> ~/.bashrc

#NEED TO DO THESE TWO ALSO
#source ~/.bashrc
#sh /opt/intel/openvino/install_dependencies/install_NCS_udev_rules.sh

# into etc/fstab     UUID=339147a8-41a4-4004-be1d-3dccfca7ecfc /mnt/gavusb/ ext4 defaults,auto,users,rw,nofail,x-systemd.device-timeout=10 0 0

