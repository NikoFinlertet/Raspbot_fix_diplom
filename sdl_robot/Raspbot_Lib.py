# coding: utf-8
import smbus
import time,random
import math

PI5Car_I2CADDR = 0x2B
class Raspbot():

    def __init__(self):
        # Инициализация I2C через smbus
        self._addr = PI5Car_I2CADDR
        self._device = smbus.SMBus(1)  # Для Raspberry Pi 1 используйте 0, для Pi 2-4 используйте 1
    
    def get_i2c_device(self, address, i2c_bus=None):
        """Совместимость с библиотеками Adafruit (опционально)"""
        return smbus.SMBus(1) if i2c_bus is None else smbus.SMBus(i2c_bus)
 # Метод для управления ультразвуковым датчиком
    def Enable_Ultrasonic(self, enable=True):
        """Включение/выключение датчика расстояния"""
        try:
            state = 1 if enable else 0
            self._device.write_i2c_block_data(self._addr, 0x07, [state])
        except Exception as e:
            print(f"Ultrasonic Error: {e}")

    # Метод для получения расстояния
    def Get_Distance(self):
        """Получение расстояния в см"""
        try:
            # Читаем 2 байта из регистров 0x1A (младший) и 0x1B (старший)
            data_low = self._device.read_byte_data(self._addr, 0x1A)
            data_high = self._device.read_byte_data(self._addr, 0x1B)
            return (data_high << 8) | data_low
        except Exception as e:
            print(f"Distance Read Error: {e}")
            return 999  # Значение при ошибке

    #Запись данных
    def write_u8(self, reg, data):
        try:
            self._device.write_byte_data(self._addr, reg, data)
        except:
            print ('write_u8 I2C error')

    def write_reg(self, reg):
        try:
            self._device.write_byte(self._addr, reg)
        except:
            print ('write_u8 I2C error')

    def write_array(self, reg, data):
        try:
            # self._device.write_block_data(self._addr, reg, data)
            self._device.write_i2c_block_data(self._addr, reg, data)
        except:
            print ('write_array I2C error')

   #Чтение данных
    def read_data_byte(self):
        try:
            buf = self._device.write_byte(self._addr)
            return buf
        except:
            print ('read_u8 I2C error')

    def read_data_array(self,reg,len):
        try:
            buf = self._device.read_i2c_block_data(self._addr,reg,len)
            return buf
        except:
            print ('read_u8 I2C error')


#Управление двигателем
    def Ctrl_Car(self, motor_id, motor_dir,motor_speed):
        try:
            if(motor_dir !=1)and(motor_dir != 0):  #参数非法,方向默认前进
                motor_dir = 0
            if(motor_speed>255):
                motor_speed = 255
            elif(motor_speed<0):
                motor_speed = 0

            reg = 0x01
            data = [motor_id, motor_dir, motor_speed]
            self.write_array(reg, data)
        except:
            print ('Ctrl_Car I2C error')

#Управление двигателем с возможностью реверса (-255~255)
    def Ctrl_Muto(self, motor_id, motor_speed):
        try:

            if(motor_speed>255):
                motor_speed = 255
            if(motor_speed<-255):
                motor_speed = -255
            if(motor_speed < 0 and motor_speed >= -255): #速度如果是负数则后退
                motor_dir = 1
            else:motor_dir = 0
            reg = 0x01
            data = [motor_id, motor_dir, abs(motor_speed)]
            self.write_array(reg, data)
        except:
            print ('Ctrl_Car I2C error')

#Управление серводвигателем
    def Ctrl_Servo(self, id, angle):
        try:
            reg = 0x02
            data = [id, angle]
            if angle < 0:
                angle = 0
            elif angle > 180:
                angle = 180
            if(id==2 and angle > 110):angle = 110
            self.write_array(reg, data)
        except:
            print ('Ctrl_Servo I2C error')

#Управление всеми светодиодами
    def Ctrl_WQ2812_ALL(self, state, color):
        try:
            reg = 0x03
            data = [state, color]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_WQ2812 I2C error')

#Управление отдельным светодиодом
    def Ctrl_WQ2812_Alone(self, number,state, color):
        try:
            reg = 0x04
            data = [number,state, color]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_WQ2812_Alone I2C error')

#Управление яркостью всех светодиодов
    def Ctrl_WQ2812_brightness_ALL(self, R, G, B):
        try:
            reg = 0x08
            data = [R,G,B]
            if R >255:
                R =255
            if G > 255:
                G = 255
            if B >255:
                B=255
            self.write_array(reg, data)
        except:
            print ('Ctrl_WQ2812 I2C error')

#Управление яркостью отдельного светодиода
    def Ctrl_WQ2812_brightness_Alone(self, number, R, G, B):
        try:
            reg = 0x09
            data = [number,R,G,B]
            if R >255:
                R =255
            if G > 255:
                G = 255
            if B >255:
                B=255
            self.write_array(reg, data)
        except:
            print ('Ctrl_WQ2812_Alone I2C error')

#Включение/выключение инфракрасного пульта
    def Ctrl_IR_Switch(self, state):
        try:
            reg = 0x05
            data = [state]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_IR_Switch I2C error')

#Включение/выключение зуммера
    def Ctrl_BEEP_Switch(self, state):
        try:
            reg = 0x06
            data = [state]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_BEEP_Switch I2C error')

#Включение/выключение ультразвукового датчика расстояния
    def Ctrl_Ulatist_Switch(self, state):
        try:
            reg = 0x07
            data = [state]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_getDis_Switch I2C error')



class LightShow:

    def __init__(self):
        self.num_lights = 14
        self.last_val = 0
        self.MAX_TIME=999999
        self.bot=Raspbot()
        self.running = True

    def execute_effect(self, effect_name,effect_duration,speed,current_color):
        try:
            if effect_name == 'river':
                self.run_river_light(effect_duration,speed)
            elif effect_name == 'breathing':
                self.breathing_light(effect_duration,speed,current_color)
            elif effect_name == 'gradient':
                self.gradient_light(effect_duration,speed)
            elif effect_name == 'random_running':
                self.random_running_light(effect_duration,speed)
            elif effect_name == 'starlight':
                self.starlight_shimmer(effect_duration,speed)
            else:
                print("Unknown effect name.")
        except KeyboardInterrupt:
            self.turn_off_all_lights()
            self.running = False

    def turn_off_all_lights(self):
        self.bot.Ctrl_WQ2812_ALL(0, 0)

    def run_river_light(self,effect_duration,speed):
        # speed = 0.01
        colors = [0, 1, 2, 3, 4, 5, 6]
        color_index = 0
        end_time = time.time()
        while self.running and time.time() - end_time < effect_duration:
            for i in range(self.num_lights - 2):
                self.bot.Ctrl_WQ2812_Alone(i, 1, colors[color_index])
                self.bot.Ctrl_WQ2812_Alone(i+1, 1, colors[color_index])
                self.bot.Ctrl_WQ2812_Alone(i+2, 1, colors[color_index])
                time.sleep(speed)
                self.bot.Ctrl_WQ2812_ALL(0, 0)
                time.sleep(speed)
            color_index = (color_index + 1) % len(colors)
        self.turn_off_all_lights()

    def breathing_light(self, effect_duration,speed,current_color):
        breath_direction = 0
        breath_count = 0
        end_time = time.time()

        while self.running and time.time() - end_time < effect_duration:

            if current_color == 0:  # Red
                r, g, b = breath_count, 0, 0
            elif current_color == 1:  # Green
                r, g, b = 0, breath_count, 0
            elif current_color == 2:  # Blue
                r, g, b = 0, 0, breath_count
            elif current_color == 3:  # Yellow
                r, g, b = breath_count, breath_count, 0
            elif current_color == 4:  # Purple
                r, g, b = breath_count, 0, breath_count
            elif current_color == 5:  # Cyan
                r, g, b = 0, breath_count, breath_count
            elif current_color == 6:  # White
                r, g, b = breath_count, breath_count, breath_count
            else:
                r, g, b = 0, 0, 0  # Default to black if invalid color code

            self.bot.Ctrl_WQ2812_brightness_ALL(r, g, b)
            time.sleep(speed)

            if breath_direction == 0:
                breath_count += 2
                if breath_count >= 255:
                    breath_count=255
                    breath_direction = 1
            else:
                breath_count -= 2
                if breath_count < 0:
                    breath_direction = 0
                    breath_count = 0
        self.turn_off_all_lights()


    def random_running_light(self,effect_duration,speed):
        # on_time = 0.01
        # off_time = 0.01
        end_time = time.time()
        while self.running and time.time() - end_time < effect_duration:
            for i in range(self.num_lights):
                color = random.randint(0, 6)
                self.bot.Ctrl_WQ2812_Alone(i, 1, color)
            time.sleep(speed)
        self.turn_off_all_lights()

    def starlight_shimmer(self,effect_duration,speed):
        min_lights_on = 1
        max_lights_on = 7
        colors = [0, 1, 2, 3, 4, 5, 6]
        end_time = time.time()
        while self.running and time.time() - end_time < effect_duration:
            for color in colors:
                start_time = time.time()
                while time.time() - start_time < 1:
                    for i in range(self.num_lights):
                        self.bot.Ctrl_WQ2812_Alone(i, 0, 0)
                    lights_on = random.sample(range(self.num_lights), k=random.randint(min_lights_on, max_lights_on))
                    for i in lights_on:
                        self.bot.Ctrl_WQ2812_Alone(i, 1, color)
                    time.sleep(speed)
                for i in range(self.num_lights):
                    self.bot.Ctrl_WQ2812_Alone(i, 0, 0)
        self.turn_off_all_lights()

    def gradient_light(self, effect_duration, speed):
        grad_color = 0
        grad_index = 0
        end_time = time.time()

        while self.running and time.time() - end_time < effect_duration:
            if grad_color % 2 == 0:
                gt_red = random.randint(0, 255)
                gt_green = random.randint(0, 255)
                gt_blue = random.randint(0, 255)

                gt_green = self.rgb_remix(gt_green)
                gt_red, gt_green, gt_blue = self.rgb_remix_u8(gt_red, gt_green, gt_blue)
                grad_color += 1

            if grad_color == 1:
                if grad_index < 14:
                    number = (grad_index % 14) + 1  # Adjusting for 1-based indexing
                    self.bot.Ctrl_WQ2812_brightness_Alone(number, gt_red, gt_green, gt_blue)
                    grad_index += 1
                if grad_index >= 14:
                    grad_color = 2
                    grad_index = 0

            elif grad_color == 3:
                if grad_index < 14:
                    number = ((14 - grad_index) % 14)   # Reverse mapping, adjusted for 1-based indexing
                    self.bot.Ctrl_WQ2812_brightness_Alone(number, gt_red, gt_green, gt_blue)
                    grad_index += 1
                if grad_index >= 14:
                    grad_color = 0
                    grad_index = 0

            time.sleep(speed)

        self.turn_off_all_lights()

    def rgb_remix(self, val):
        if abs(val - self.last_val) < val % 30:
            val = (val + self.last_val) % 255
        self.last_val = val % 255
        return self.last_val

    def rgb_remix_u8(self, r, g, b):
        if r > 50 and g > 50 and b > 50:
            index = random.randint(0, 2)
            if index == 0:
                r = 0
            elif index == 1:
                g = 0
            elif index == 2:
                b = 0
        return r, g, b

    def calculate_breath_color(self, color_code, breath_count):
        max_brightness = 255
        if color_code == 0:  # Red
            return max_brightness, breath_count, 0
        elif color_code == 1:  # Green
            return max_brightness, 0, breath_count
        elif color_code == 2:  # Blue
            return max_brightness, 0, 0, breath_count
        elif color_code == 3:  # Yellow
            return max_brightness, breath_count, breath_count, 0
        elif color_code == 4:  # Purple
            return max_brightness, breath_count, 0, breath_count
        elif color_code == 5:  # Cyan
            return max_brightness, 0, breath_count, breath_count
        elif color_code == 6:  # White
            return max_brightness, breath_count, breath_count, breath_count
        else:
            return 0, 0, 0  # Default to black if invalid color code

    def stop(self):
        self.running = False

# test
#car = Raspbot()

#Read line tracking sensor address (this value is 1 byte)
# track =car.read_data_array(0x0a,1)
# track = int(track[0])
# x1 = (track>>3)&0x01
# x2 = (track>>2)&0x01
# x3 = (track>>1)&0x01
# x4 = (track)&0x01
# print(track,x1,x2,x3,x4)


# Read ultrasonic sensor address (this value is 2 bytes)
# car.Ctrl_Ulatist_Switch(1)#open
# time.sleep(1)
# diss_H =car.read_data_array(0x1b,1)[0]
# diss_L =car.read_data_array(0x1a,1)[0]
# dis = diss_H<< 8 | diss_L
# print(dis+"mm")
# car.Ctrl_Ulatist_Switch(0)#close

#Read infrared remote control value
# car.Ctrl_IR_Switch(1)
# time.sleep(3)
# data =car.read_data_array(0x0c,1)
# print(data)
# car.Ctrl_IR_Switch(0)


#Buzzer test
# car.Ctrl_BEEP_Switch(1)
# time.sleep(1)
# car.Ctrl_BEEP_Switch(0)
# time.sleep(1)

#Motor test
# car.Ctrl_Car(0,0,150) #L1电机 前进 150速度
# car.Ctrl_Car(1,0,150) #L2电机 前进 150速度
# car.Ctrl_Car(2,0,150) #R1电机 前进 150速度
# car.Ctrl_Car(3,0,150) #R2电机 前进 150速度
# time.sleep(1)
# car.Ctrl_Car(0,1,50) #L1电机 后退 50速度
# time.sleep(1)
# car.Ctrl_Car(0,0,0) #L1电机 停止
# car.Ctrl_Car(1,0,0) #L2电机 停止
# car.Ctrl_Car(2,0,0) #R1电机 停止
# car.Ctrl_Car(3,0,0) #R2电机 停止


#Servo motor test
# car.Ctrl_Servo(1,0) #s1 0度
# car.Ctrl_Servo(2,180) #s2 180度
# time.sleep(1)
# car.Ctrl_Servo(1,180) #s1 180度
# car.Ctrl_Servo(2,0) #s2 0度
# time.sleep(1)

#LED strip test
# car.Ctrl_WQ2812_ALL(1,0)#红色
# time.sleep(1)
# car.Ctrl_WQ2812_ALL(1,1)#绿色
# time.sleep(1)
# car.Ctrl_WQ2812_ALL(1,2)#蓝色
# time.sleep(1)
# car.Ctrl_WQ2812_ALL(1,3)#黄色
# time.sleep(1)
# car.Ctrl_WQ2812_ALL(0,0) #关闭

#Individual LED test
# car.Ctrl_WQ2812_Alone(1,1,0)#1号红色
# time.sleep(1)
# car.Ctrl_WQ2812_Alone(2,1,3)#1号黄色
# time.sleep(1)
# car.Ctrl_WQ2812_Alone(1,0,3)#1号关
# time.sleep(1)
# car.Ctrl_WQ2812_Alone(10,1,2)#10号绿色
# time.sleep(1)
# car.Ctrl_WQ2812_ALL(0,0) #关闭

#Brightness control test (all LEDs)
# for i in range(255):
#     car.Ctrl_WQ2812_brightness_ALL(i,0,0)
#     time.sleep(0.01)