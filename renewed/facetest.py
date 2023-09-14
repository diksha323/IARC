import cv2
import face_recognition
import pickle


with open('face_data.pkl', 'rb') as f:
    all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
face_names = list(all_face_encodings.keys())

face_encod=[]
for f in list(all_face_encodings.values()):
    # print(type(all_face_encodings[f]))
    face_encod.append(face_recognition.face_encodings(f))

# Initialize the webcam

cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Find faces in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        
        name = "Unknown"
        # for known_name, known_face_encoding in known_faces.items():
        for known_face_encoding,known in zip(face_encod,face_names):
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)# Compare the face encoding to known faces
            if True in matches:
                name = known
            # name="hhh"

        # Draw a rectangle and label around the recognized face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Display the frame with recognized faces
    cv2.imshow('Live Face Recognition', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
