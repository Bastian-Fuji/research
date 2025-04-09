import tkinter as tk
import serial
import time
from suit_raw_controller import send_data_to_arduino

class SuitManualControllGUI:
    def __init__(self, arduino_serial):
        self.arduino_serial = arduino_serial
        self.upperbody_direction = "0000"
        self.lower_body_direction = "00"
        self.suit_direction = self.upperbody_direction + self.lower_body_direction
        self.root = tk.Tk()
        self.root.geometry("980x550")
        self.root.title("Suit Manual Control")

        #Upper Body Buttons
        self.upper_body_label = tk.Label(self.root, text = "Upper Body Direction", font=("Helvetica", 20))
        self.btn_neutral = tk.Button(self.root, text="Neutral", command=self.neutral, width=20, font=("Helvetica", 20))
        self.btn_bend_forward = tk.Button(self.root, text="Bend Forward", command=self.bend_forward, width=20, font=("Helvetica", 20))
        self.btn_bend_right = tk.Button(self.root, text="Bend Right", command=self.bend_right, width=20, font=("Helvetica", 20))
        self.btn_bend_left = tk.Button(self.root, text="Bend Left", command=self.bend_left, width=20, font=("Helvetica", 20))
        self.btn_twist_right = tk.Button(self.root, text="Twist Right", command=self.twist_right, width=20, font=("Helvetica", 20))
        self.btn_twist_left = tk.Button(self.root, text="Twist Left", command=self.twist_left, width=20, font=("Helvetica", 20))

        #Upper Body Force Slider
        self.upper_body_force_label = tk.Label(self.root, text = "Upper Body Force", font=("Helvetica", 20))
        self.slider = tk.Scale(self.root, from_=0, to=9, orient="horizontal", bg='lightgray', fg='black', length=800, font=("Helvetica", 20))
        self.empty1 = tk.Label(self.root, text = "", font=("Helvetica", 20))


        #Lower Body Buttons
        self.lower_body_label = tk.Label(self.root, text = "Lower Body Direction", font=("Helvetica", 20))
        self.btn_up = tk.Button(self.root, text="Up", command=self.up, width=20, font=("Helvetica", 20))
        self.btn_squat= tk.Button(self.root, text="Squat", command=self.squat, width=20, font=("Helvetica", 20))
        self.btn_neutral_lower_body = tk.Button(self.root, text="Neutral", command=self.neutral_lower_body, width=20, font=("Helvetica", 20))

        #Lower Body Force Slider
        self.lower_body_force_label = tk.Label(self.root, text = "Lower Body Force", font=("Helvetica", 20))
        self.slider_lower_body = tk.Scale(self.root, from_=0, to=9, orient="horizontal", bg='lightgray', fg='black', length=800, font=("Helvetica", 20))
        self.empty2 = tk.Label(self.root, text = "", font=("Helvetica", 20))
        
        #Debug command sent to arduino
        self.debugtext = tk.Label(self.root, text = self.suit_direction , font=("Helvetica", 10))
        
        #Layout
        #Layout Upper Body
        self.upper_body_label.grid(row=0, column=1)
        self.btn_neutral.grid(row=1, column=0)
        self.btn_bend_forward.grid(row=1, column=1)
        self.btn_bend_right.grid(row=1, column=2)
        self.btn_bend_left.grid(row=2, column=0)
        self.btn_twist_right.grid(row=2, column=1)
        self.btn_twist_left.grid(row=2, column=2)

        self.upper_body_force_label.grid(row=3, column=1)
        self.slider.grid(row=4, columnspan=3)
        self.empty1.grid(row=5, columnspan=3)

        #Layout Lower Body
        self.lower_body_label.grid(row=6, column=1)
        self.btn_up.grid(row=7, column=0)
        self.btn_squat.grid(row=7, column=1)
        self.btn_neutral_lower_body.grid(row=7, column=2)

        self.lower_body_force_label.grid(row=8, column=1)
        self.slider_lower_body.grid(row=9, columnspan=3)
        self.empty2.grid(row=10, columnspan=3)

        #Layout Debug
        self.debugtext.grid(row=11, columnspan=3)

    def get_slider_value(self):
        slider_upper_body_value = str(int(self.slider.get()))
        slider_lower_body_value = str(int(self.slider_lower_body.get()))
        return slider_upper_body_value, slider_lower_body_value

    def update_suit_direction(self):
        slider_upper_body_value, slider_lower_body_value = self.get_slider_value()
        self.upperbody_direction = self.upperbody_direction.replace("r", slider_upper_body_value)
        self.lower_body_direction = self.lower_body_direction.replace("r", slider_lower_body_value)

        self.suit_direction = f"{self.upperbody_direction}{self.lower_body_direction}"
        send_data_to_arduino(self.suit_direction, self.arduino_serial)
        self.debugtext.config(text=self.suit_direction)


    def neutral(self):
        self.upperbody_direction = "11r1"
        self.update_suit_direction()


    def bend_forward(self):
        self.upperbody_direction = "20r1"
        self.update_suit_direction()

    def bend_right(self):
        self.upperbody_direction = "12r1"
        self.update_suit_direction()

    def bend_left(self):
        self.upperbody_direction = "10r1"
        self.update_suit_direction()

    def twist_right(self):
        self.upperbody_direction = "00r0"
        self.update_suit_direction()

    def twist_left(self):
        self.upperbody_direction = "00r2"
        self.update_suit_direction()

    def up(self):
        self.lower_body_direction = "r0"
        self.update_suit_direction()

    def squat(self):
        self.lower_body_direction = "0r"
        self.update_suit_direction()

    def neutral_lower_body(self):
        self.lower_body_direction = "00"
        self.update_suit_direction()


# Run the application
def main():
    print()
    arduino_serial = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(1)  # Wait for the connection to establish

    app = SuitManualControllGUI(arduino_serial)
    app.root.mainloop()
    arduino_serial.close()
    print("Arduino connection closed")

if __name__ == "__main__":
    main()