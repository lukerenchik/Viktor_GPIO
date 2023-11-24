from GPIODetector import HardwareInterface
import time


class LukesButton(HardwareInterface):

	def buttonPressed(self, nButtonPresses):
		# add stuff here
		print(nButtonPresses)
		print("this is luke's button function press")
	
	def buttonReleased(self, nButtonReleases):
		# add stuff here
		print(nButtonReleases)
		print("this is luke's button function release")

if __name__ == "__main__":

	PIN_NUMBER = 5

	lukeButton = LukesButton(PIN_NUMBER)
	lukeButton.createButtonThread()
	
	
	while 1:
		#print(time.perf_counter())
		time.sleep(0.001)
