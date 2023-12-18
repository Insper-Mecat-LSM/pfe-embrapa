import time

class PhSensor:
  def __init__(self, pin, samples):
        self.pin = pin
        self.samples = samples
  
  def start_measure(self):
    measurings = 0
    
    for i in range(self.samples):
        measurings += self.pin.read()
        time.sleep(1)
    
    voltage = (measurings / self.samples) * (3.3/4096.0)
    calculus = -4096 * (voltage / 3.3) + 4096
    pH = calculus * 14 / 4096
    pH_calibrado = 2.0211 * pH -7.6140
    print("Voltagem: ", voltage, end = ',')
    print("pH: ", pH_calibrado)
    return pH_calibrado