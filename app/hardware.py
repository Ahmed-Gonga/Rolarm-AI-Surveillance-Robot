import time

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except Exception:
    GPIO = None
    GPIO_AVAILABLE = False

class RobotHardware:
    def __init__(self, cfg, db=None):
        self.cfg = cfg
        self.db = db
        self.mock = cfg.get('mock_hardware', False) or not GPIO_AVAILABLE
        self.motion = 'stop'
        self.speed = int(cfg.get('default_speed_percent', 70))
        self._pwm = {}
        if not self.mock:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            pins = cfg['motor_pins']
            for key in ['IN1','IN2','IN3','IN4']:
                GPIO.setup(int(pins[key]), GPIO.OUT)
                GPIO.output(int(pins[key]), GPIO.LOW)
            for key in ['ENA','ENB']:
                if cfg.get('use_pwm_speed', True) and key in pins:
                    GPIO.setup(int(pins[key]), GPIO.OUT)
                    pwm = GPIO.PWM(int(pins[key]), 1000)
                    pwm.start(self.speed)
                    self._pwm[key] = pwm
            for pin_name in ['gas_sensor_pin','fire_sensor_pin','pir_sensor_pin']:
                GPIO.setup(int(cfg[pin_name]), GPIO.IN)
            for pin_name in ['buzzer_pin','led_pin']:
                GPIO.setup(int(cfg[pin_name]), GPIO.OUT)
                GPIO.output(int(cfg[pin_name]), GPIO.LOW)

    def set_speed(self, percent):
        self.speed = max(0, min(100, int(percent)))
        for pwm in self._pwm.values():
            pwm.ChangeDutyCycle(self.speed)
        return self.speed

    def _write_motors(self, vals):
        if self.mock: return
        pins = self.cfg['motor_pins']
        for key, val in zip(['IN1','IN2','IN3','IN4'], vals):
            GPIO.output(int(pins[key]), GPIO.HIGH if val else GPIO.LOW)

    def move(self, direction):
        direction = direction.lower()
        mapping = {
            'forward': (1,0,1,0), 'backward': (0,1,0,1),
            'left': (0,1,1,0), 'right': (1,0,0,1),
            'stop': (0,0,0,0)
        }
        if direction not in mapping: direction = 'stop'
        self._write_motors(mapping[direction])
        self.motion = direction
        return direction

    def stop(self):
        return self.move('stop')

    def buzzer(self, on):
        if not self.mock:
            GPIO.output(int(self.cfg['buzzer_pin']), GPIO.HIGH if on else GPIO.LOW)
            GPIO.output(int(self.cfg['led_pin']), GPIO.HIGH if on else GPIO.LOW)
        return bool(on)

    def read_sensors(self):
        if self.mock:
            return {'gas': False, 'fire': False, 'motion': False, 'mock': True}
        gas = GPIO.input(int(self.cfg['gas_sensor_pin'])) == int(self.cfg['gas_active_level'])
        fire = GPIO.input(int(self.cfg['fire_sensor_pin'])) == int(self.cfg['fire_active_level'])
        motion = GPIO.input(int(self.cfg['pir_sensor_pin'])) == int(self.cfg['pir_active_level'])
        return {'gas': bool(gas), 'fire': bool(fire), 'motion': bool(motion), 'mock': False}

    def cleanup(self):
        self.stop(); self.buzzer(False)
        for pwm in self._pwm.values():
            pwm.stop()
        if not self.mock:
            GPIO.cleanup()
