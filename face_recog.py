
import cv2
import face_recognition
# save numpy array as npy file
from numpy import load
# from numpy import save



font=cv2.FONT_HERSHEY_DUPLEX

# img1=cv2.imread('me.jpg')
# img1=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
# # cv2.imshow("live",img1)
# # cv2.waitKey(0)

# picture_of_me = face_recognition.face_locations(img1)
# my_face_encoding = face_recognition.face_encodings(img1,picture_of_me)[0]
# # define data
# data = asarray(my_face_encoding)
# # save to npy file
# save('data.npy', data)
my_face_encoding = load('data.npy')
video=cv2.VideoCapture(0)
while True:
	ret,video_data=video.read()
	img=cv2.cvtColor(video_data,cv2.COLOR_BGR2RGB)
	face=face_recognition.face_locations(img)
	encod=face_recognition.face_encodings(img,face)

	for f,face_encoding in zip(face,encod):
		y,a,b,x=f
		cv2.rectangle(video_data,(x,y),(a,b),(255,0,255),2)
		cv2.rectangle(video_data, (x, b - 25), (a, b), (0, 0, 255), cv2.FILLED)
		results = face_recognition.compare_faces(my_face_encoding, encod)
		
		if results[0] == True:
			cv2.putText(video_data, 'subun', (x + 3, b - 3), font, 1.0, (255, 255, 255), 2)

		else:
			cv2.putText(video_data, 'uknown', (x + 3, b - 3), font, 1.0, (255, 255, 255), 2)

		


		

	 
	    
	cv2.imshow("live",video_data)
		
	if cv2.waitKey(10)==ord("s"):
		break
video.release()		
	
