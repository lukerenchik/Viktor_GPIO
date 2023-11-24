import RPi.GPIO as io
import asyncio
from threading import Thread
import time

class HardwareInterface():

	def __init__(self, _pinNumber):
		self.pinNumber = _pinNumber
		io.setmode(io.BOARD)
		io.setup(_pinNumber, io.IN, pull_up_down=io.PUD_UP)
		self._pressCounter = 0
		self._releaseCounter = 0
		
		# button starts raised
		self._buttonState = 1
		
		self._isDirty = False
		
	@property
	def buttonState(self):
		# mark the state as not Dirty
		self._isDirty = False
		return self._buttonState
		
	@buttonState.setter
	def buttonState(self, newState):
		self._buttonState = newState
		self._isDirty = True
		
	async def checkButtonState(self):
		while True:
			# keep track of edge detection
			previousButtonState = self.buttonState
			# read the state of the button at the pin number
			self.buttonState = io.input(self.pinNumber)
			
			if (previousButtonState == self.buttonState):
				# button has not changed state
				await asyncio.sleep(0.03)
				continue
			
			# call the change state function
			if self.buttonState == 0:
				self._pressCounter += 1
				# button is pressed state when low
				self.buttonPressed(self._pressCounter)
				# debounce the button
			else:
				self._releaseCounter += 1
				# button is released when high
				self.buttonReleased(self._releaseCounter)
				# debounce the button
			
	def startButtonDetection(self):
		# start the button detection
		asyncio.run(self.checkButtonState())
		#asyncio.ensure_future(self.checkButtonState())
		
		
	def createButtonThread(self): 
		self.buttonThread = Thread(target=self.startButtonDetection)
		self.buttonThread.start()
	
	# callback function
	def buttonPressed(self, nButtonPresses):
		print(f"the button is pressed {self.pressCounter} times")
	
	def buttonReleased(self, nButtonReleases):
		print(f"the button is released {self.releaseCounter} times")
	
if __name__ == "__main__":
	
	# set the hardware macros
	BUTTON_PIN = 5
	
	# create the physical pushbutton object
	PhysicalButton = HardwareInterface(BUTTON_PIN)
	
	PhysicalButton.createButtonThread()
	
	while 1:
		print("no button press")
		time.sleep(5)
		
		
		
		
	
	
	
