# robot
this package need : ROS indigo
                    I2C tools 
                    pyserial
                    enum
                    python-tk
                    
Installation:
  ROS:
    install ROS indigo http://wiki.ros.org/indigo/Installation/UbuntuARM
  I2C:
    first you need to update the kernel
    $ sudo odroid-utility.sh 
    in Update your Kernel/Firmware select Update Kernel
    
    $ sudo apt-get update
    $ sudo apt-get install python-smbus
    $ sudo apt-get install i2c-tools
    
    configurate the i2c to start automaticly
    $ sudo nano /etc/modules
    add :
      i2c-gpio-custom bus0=4,209,210      
      i2c-dev
      aml_i2c
    reboot your system 
      $ sudo reboot
  
  Python packages:
    sudo apt-get install python-pip
    sudo pip install pyserial
    sudo pip install enum
    sudo apt-get install python-tk

now use git clone to download the package:
  $ cd catkin_ws/src
  $ git clone https://github.com/mekhtiche/robot.git
  $ cd ..
  $ catkin_make
  source the work space
    $ sudo nano .bashrc
    in the end of the file add "source ~/catkin_ws/devel/setup.bash"
    
    
To launch the robot:
  $ roslaunch robot Robot_start.launch

To record sign:
  $ roslaunch robot Recording.launch
  
  
if you have permission denied error you need to change the permission of Servo_driver.py and finger.py
  $ cd catkin_ws/src/robot/driver
  $ chmod 775 Servo_driver.py 
  $ cd catkin_ws/src/robot/recording
  $ chmod 775 finger.py 


