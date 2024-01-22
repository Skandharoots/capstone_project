#login: kissicpmachine
#password: kissicpmachine

sudo apt update
sudo apt upgrade

#C++
sudo apt install g++
sudo apt install cmake
sudo apt install gdb
sudo apt-get install build-essential

#Python
sudo apt install python3
sudo apt install python3-pip

#KISS_ICP libs
sudo apt install libeigen3-dev libtbb-dev pybind11-dev ninja-build 

#Git
sudo apt install git

# git clone https://gitlab.com/capstonetf2023/capstonecode.git

pip install "kiss-icp[all]"

pip install -U rosbags

make install

#Information regarding an error "Core dumped" resulting from missing AVX and AVX2 flags on newer cpus.
#First you need to disable hyper-v. To do so open command prompt on windows as an administrator.
#Enter the following instructions:

#bcdedit /set hypervisorlaunchtype off
#DISM /Online /Disable-Feature:Microsoft-Hyper-V
#shutdown -s -t 2

#Wait a few moments before turning the pc back on
#In the windows search type "core isolation"
#Disable it and restart the pc
#Turn on the vm and simply run the main.py script