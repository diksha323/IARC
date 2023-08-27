#!/usr/bin/env python3
import smbus
import rospy		
import aerial_stabilization.msg as msg    

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
g = 9.80665
bus = smbus.SMBus(1)
Device_Address = 0x68

def mpu_init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)
        
def read_raw_data(addr):

	#Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    #concatenate higher and lower value
    value = ((high << 8) | low)
        
    #to get signed value from mpu6050
    if(value > 32768):
                value = value - 65536
    return value


def mpu_msg():
    pub = rospy.Publisher('mpu_6050_msg', msg.Mpu6050_msg, queue_size=10)
    rospy.init_node('mpu6050_msg_publisher', anonymous=True)
    mpu_data = msg.Mpu6050_msg()
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
	    #Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        
        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
        
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = (acc_x/16384.0)*g
        Ay = (acc_y/16384.0)*g
        Az = (acc_z/16384.0)*g
        
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0

        mpu_data.Ax = Ax
        mpu_data.Ay = Ay
        mpu_data.Az = Az

        mpu_data.Gx = Gx
        mpu_data.Gy = Gy
        mpu_data.Gz = Gz
        rospy.loginfo(mpu_data)
        pub.publish(mpu_data)

#        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 

        rate.sleep()

if __name__ == '__main__':
    try:
        mpu_init()
        mpu_msg()
    except rospy.ROSInterruptException:
        pass