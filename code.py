import board
import analogio
import digitalio
import pwmio
import time
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

led = pwmio.PWMOut(board.LED)
led_assigned_pedal = 0

pedal_count = 4
# sustain, sostenuto, harmonic and una corda
pedal_enable = [1, 0, 0, 1]
pedal_cc = [64, 66, 69, 67]
pedal_pin = [analogio.AnalogIn(board.A0),
             analogio.AnalogIn(board.A1),
             analogio.AnalogIn(board.A2),
             digitalio.DigitalInOut(board.GP22)]
pedal_value = [0, 0, 0, 0]

for i in range(pedal_count):
    if type(pedal_pin[i]) == digitalio.DigitalInOut:
        pedal_pin[i].direction = digitalio.Direction.INPUT
        pedal_pin[i].pull = digitalio.Pull.UP

while True:
    for i in range(pedal_count):
        if pedal_enable[i]:
            print(pedal_pin[i].value)
            val = (pedal_pin[i].value // 512
                   if type(pedal_pin[i]) == analogio.AnalogIn
                   else pedal_pin[i].value * 127)

            # send midi message only if the value is changed
            if val != pedal_value[i]:
                if i == led_assigned_pedal:
                    led.duty_cycle = val * 512
                midi.send(ControlChange(pedal_cc[i], val))
                pedal_value[i] = val
    time.sleep(0.002)
