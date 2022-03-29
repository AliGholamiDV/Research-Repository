import tkinter as tk
from tkinter import font
from zaber_motion import Units, Library, RotationDirection
from zaber_motion.ascii import Connection
import time

# CONSTANTS #########################################
Gear_ratio = 3
Token_radius = 0.5 # [m] 		# Token distance from the rotation axis
Direction = 1 				# -1 for clockwise and 1 for counterclockwise
Acceleration = 7 			#RPM/s -- minimum value is ~7 RPM/s -- Increase by multiplies of the minimum value (eg. 7,14,21,..)
Deceleration = 7 			#RPM/s -- minimum value is ~7 RPM/s -- Increase by multiplies of the minimum value (eg. 7,14,21,..)

#####################################################

Library.enable_device_db_store()   	# The library connects to the internet to retrieve information about Zaber devices.

with Connection.open_serial_port("/dev/ttyACM0") as connection:
    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))
    device = device_list[0]
    axis = device.get_axis(1)
    
    def move():
        axis.generic_command("driver enable") 	# Clears all the warning flags and enables the driver. 
        axis.generic_command("activate")	# Activates the peripheral
        axis.unpark()
        print("\nRunning forward...")
        Motor_RPS = Direction * Speed_scale.get() * Gear_ratio / Token_radius # Radian per second
        axis.move_velocity(Motor_RPS, unit = Units.ANGULAR_VELOCITY_RADIANS_PER_SECOND)
        
    def stop():
        print("Stopping...")
        axis.stop()
        axis.park()


# GUI #################################################

    root = tk.Tk()
    canvas = tk.Canvas(root, height = 800, width=1400)
    canvas.pack()
    INF = 1000

    frame = tk.Frame(root, bg='#F77029')
    frame_pb = tk.Frame(frame, bg='#F77029')  # Push Button
    frame_sb = tk.Frame(frame, bg='#F77029')  # Stop Button
    frame_1 = tk.Frame(frame, bg='#F77029')   # Velocity Bar		
    frame.place(relx = 0.01, rely = 0.01, relwidth = 0.98, relheight= 0.98)
    frame_pb.place(relx = 0.05, rely = 0.05, relwidth = 0.2, relheight= 0.2)
    frame_sb.place(relx = 0.05, rely = 0.75, relwidth = 0.2, relheight= 0.2)
    frame_1.place(relx = 0.3, rely = 0.05, relwidth = 0.6, relheight= 0.2)
    Play_button = tk.Button(frame_pb, width = INF, height = INF, text = "START", font = ("Gabriola", 32), \
                            bg='green', fg='white', activebackground = "green", command = move)
    Stop_button = tk.Button(frame_sb, width = INF, height = INF, text = "STOP", font = ("Gabriola", 32), \
                            bg='red', fg='white', activebackground = "red", command = stop)
    Speed_scale = tk.Scale(frame_1, label = "Token Linear Speed [m/s]", orient = "horizontal", font = ("Gabriola", 24), \
                           length = INF, from_=0, to=2.0, resolution = 0.1, width = 50, \
                           bg = "#060000", fg ="#FFFFFF", troughcolor = "#CE4100", activebackground = "#450F00", \
                           cursor = "heart", repeatdelay = 800, sliderlength = 60)
    Speed_scale.pack()
    Play_button.pack()
    Stop_button.pack(side = "bottom")

            
    root.mainloop()
