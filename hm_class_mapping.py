import numpy as np
import cv2
import copy
import hm_class_counting
from imutils.video import VideoStream
from imutils.video import FPS
import time
import dlib

class Mkmap():
	vidpath=str()
	outvidpath=str()
	modelpath=str('MobileNetSSD_deploy.caffemodel')
	prototxtpath=str('MobileNetSSD_deploy.prototxt.txt')
	def __init__(self, vidpath):
		self.vidpath=vidpath
	def mapping1(self):
		fps = '30'
		cap = cv2.VideoCapture(self.vidpath)
		#outfile = 'heatmap.mp4'


		while True:
			try:
				_, f0 = cap.read()
				f = cv2.resize(f0, (0,0), fx=0.5, fy=0.5) 
				f = cv2.GaussianBlur(f, (1, 1), 0.5, 0.5)
				f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
				cnt = 0
				res = 0.05*f
				res = res.astype(np.float64)
				break
			except:
				print('s')


		fgbg = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=500,detectShadows=True)

		#writer = FFmpegWriter(outfile, outputdict={'-r': fps})
		#writer = FFmpegWriter(outfile)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
		cnt = 0
		sec = 0
		while True:
			# if sec == duration: break
			"""cnt += 1
			if cnt % int(fps) == 0:
				print(sec)
				sec += 1"""
			ret, frame = cap.read()
			frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
			if not ret: break
			fgmask = fgbg.apply(frame, None, 0.3)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# if cnt == 30: res
			gray = cv2.GaussianBlur(gray, (1, 1), 1, 1)
			gray = gray.astype(np.float64)
			fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
			fgmask = fgmask.astype(np.float64)
			res += (40 * fgmask + gray) * 0.01
			res_show = res / res.max()
			res_show = np.floor(res_show * 255)
			res_show = res_show.astype(np.uint8)
			res_show = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)
			cv2.imshow('s', res_show)
			# if sec < start: continue
		#	try:
		#		writer.writeFrame(res_show)
		#	except:
		#		writer.close()
		#		break
			
			k = cv2.waitKey(30) & 0xff
			if k == 27:
				break

		#writer.close()
		cap.release()
		cv2.destroyAllWindows()

	def mapping1rt(self):
		fps = '30'
		cap = cv2.VideoCapture(0)
		#outfile = 'heatmap.mp4'


		while True:
			try:
				_, f0 = cap.read()
				f = cv2.resize(f0, (0,0), fx=0.5, fy=0.5) 
				f = cv2.GaussianBlur(f, (1, 1), 0.5, 0.5)
				f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
				cnt = 0
				res = 0.05*f
				res = res.astype(np.float64)
				break
			except:
				print('s')


		fgbg = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=500,detectShadows=True)

		#writer = FFmpegWriter(outfile, outputdict={'-r': fps})
		#writer = FFmpegWriter(outfile)

		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
		cnt = 0
		sec = 0
		while True:
			# if sec == duration: break
			"""cnt += 1
			if cnt % int(fps) == 0:
				print(sec)
				sec += 1"""
			ret, frame = cap.read()
			frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
			if not ret: break
			fgmask = fgbg.apply(frame, None, 0.3)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# if cnt == 30: res
			gray = cv2.GaussianBlur(gray, (1, 1), 1, 1)
			gray = gray.astype(np.float64)
			fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
			fgmask = fgmask.astype(np.float64)
			res += (40 * fgmask + gray) * 0.01
			res_show = res / res.max()
			res_show = np.floor(res_show * 255)
			res_show = res_show.astype(np.uint8)
			res_show = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)
			cv2.imshow('s', res_show)
			# if sec < start: continue
		#	try:
		#		writer.writeFrame(res_show)
		#	except:
		#		writer.close()
		#		break
			
			k = cv2.waitKey(30) & 0xff
			if k == 27:
				break

		#writer.close()
		cap.release()
		cv2.destroyAllWindows()


	def mapping2(self):
		motionVid=Motion(self.vidpath)
		motionVid.prep()
		motionVid.run()
		motionVid.write()

	def mapping3(self):
		heatm=HeatMotion(self.vidpath)
		heatm.detect()

	def countf(self):
		cn=hm_class_counting.person_count(self.prototxtpath, self.modelpath, self.vidpath, self.outvidpath , 0.4, 30)
		cn.track()
		cn.counting()



class Motion:
	
	def __init__(self, vidpath):	
					print("Motion Detection Object Created")	
					#input file name of video
					self.inname= vidpath
	
					#file name to save
					self.outname = "C:\\MotionMeerkat"
	
	def prep(self):
		
		#just read the first frame to get height and width
		cap = cv2.VideoCapture(self.inname)	 
				
		ret,self.orig_image = cap.read()
		width = np.size(self.orig_image, 1)
		height = np.size(self.orig_image, 0)
		frame_size=(height, width)		   
		
		#make accumulator image of the same size
		self.accumulator =  np.zeros((height, width), np.float32) # 32 bit accumulator
		#print('1 cl')

				
	def run(self):
		cap = cv2.VideoCapture(self.inname)
		fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=80,detectShadows=False)
		while(1):
			ret, frame = cap.read()
			if not ret:
				break
			fgmask = fgbg.apply(frame)
			self.accumulator=self.accumulator+fgmask
		#print('2 cl')
	def write(self):
		
		self.ab=cv2.convertScaleAbs(255-np.array(self.accumulator,'uint8'))  
		
		#only get reasonable high values, above mean
		ret,self.acc_thresh=cv2.threshold(self.ab,self.ab.mean(),255,cv2.THRESH_TOZERO)
		
		#make a color map
		acc_col = cv2.applyColorMap(self.acc_thresh,cv2.COLORMAP_HOT)
		
		cv2.imwrite(str(self.outname + "\\heatmap.jpg"),acc_col)
		
		#add to original frame
		backg = cv2.addWeighted(np.array(acc_col,"uint8"),0.45,self.orig_image,0.55,0)
		
		cv2.imwrite(str(self.outname + "\\heatmap_background.jpg"),backg)
		#print('1 f')

class HeatMotion():
	vidpath = str()
	def __init__(self, vidpath):
		self.vidpath = vidpath
	def detect(self):

		cap = cv2.VideoCapture(self.vidpath)
		# pip install opencv-contrib-python
		fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

		# number of frames is a variable for development purposes, you can change the for loop to a while(cap.isOpened()) instead to go through the whole video
		num_frames = 350

		first_iteration_indicator = 1
		for i in range(0, num_frames):
			'''
			There are some important reasons this if statement exists:
				-in the first run there is no previous frame, so this accounts for that
				-the first frame is saved to be used for the overlay after the accumulation has occurred
				-the height and width of the video are used to create an empty image for accumulation (accum_image)
			'''
			if (first_iteration_indicator == 1):
				ret, frame = cap.read()
				first_frame = copy.deepcopy(frame)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				height, width = gray.shape[:2]
				accum_image = np.zeros((height, width), np.uint8)
				first_iteration_indicator = 0
			else:
				ret, frame = cap.read()  # read a frame
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale

				fgmask = fgbg.apply(gray)  # remove the background

				# for testing purposes, show the result of the background subtraction
				# cv2.imshow('diff-bkgnd-frame', fgmask)

				# apply a binary threshold only keeping pixels above thresh and setting the result to maxValue.  If you want
				# motion to be picked up more, increase the value of maxValue.  To pick up the least amount of motion over time, set maxValue = 1
				thresh = 2
				maxValue = 2
				ret, th1 = cv2.threshold(fgmask, thresh, maxValue, cv2.THRESH_BINARY)
				# for testing purposes, show the threshold image
				# cv2.imwrite('diff-th1.jpg', th1)

				# add to the accumulated image
				accum_image = cv2.add(accum_image, th1)
				# for testing purposes, show the accumulated image
				# cv2.imwrite('diff-accum.jpg', accum_image)

				# for testing purposes, control frame by frame
				# raw_input("press any key to continue")

			# for testing purposes, show the current frame
			# cv2.imshow('frame', gray)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# apply a color map
		# COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
		color_image = im_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
		# for testing purposes, show the colorMap image
		# cv2.imwrite('diff-color.jpg', color_image)

		# overlay the color mapped image to the first frame
		result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

		# save the final overlay image
		cv2.imwrite('diff-overlay.jpg', result_overlay)

		# cleanup
		cap.release()
		cv2.destroyAllWindows()