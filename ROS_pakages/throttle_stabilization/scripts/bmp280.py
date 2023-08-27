#!/usr/bin/env python3
import rospy
import board
import adafruit_bmp280
import throttle_stabilization.msg as msg

def bmp_msg():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    bmp280.sea_level_pressure = 1013.25
    pub = rospy.Publisher('bmp280_msg', msg.Bmp280_msg, queue_size=10)
    rospy.init_node('bmp280_msg_publisher', anonymous=True)
    bmp_data = msg.Bmp280_msg()
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
#        print("\nTemperature: %0.1f C" % bmp280.temperature)
#       print("Pressure: %0.1f hPa" % bmp280.pressure)
#       print("Altitude = %0.2f meters" % bmp280.altitude)
        bmp_data.pressure = bmp280.pressure
        bmp_data.temperature = bmp280.temperature
        bmp_data.altitude = bmp280.altitude
        rospy.loginfo(bmp_data)
        pub.publish(bmp_data)
        rate.sleep()

if __name__ == '__main__':
    try:
        bmp_msg()
    except rospy.ROSInterruptException:
        pass