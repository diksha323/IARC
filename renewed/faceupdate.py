import cv2
import os

# Create a directory to store face data
if not os.path.exists('face_data'):
    os.makedirs('face_data')

# Initialize the face recognition model (you can use other models like dlib or MTCNN)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize an empty dictionary to store face data (name and face image)
face_data = {}

# Function to capture and store faces
def capture_faces(name, num_samples=1):
    cap = cv2.VideoCapture(0)  # 0 for default camera (you can change this to a video file)
    count = 0
    
    while count < num_samples:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        cv2.imshow('Capturing Faces', frame)
        
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            for (x, y, w, h) in faces:
                face_roi = frame[y:y + h, x:x + w]
                face_data[name] = face_roi
                cv2.imwrite(f'face_data/{name}.jpg', face_roi)
                count += 1

        
        

    cap.release()
    cv2.destroyAllWindows()

# Input names and capture faces
num_people = int(input("Enter the number of people: "))
for i in range(num_people):
    name = input(f"Enter the name of person {i + 1}: ")
    print("click ""c"" to save")
    capture_faces(name)

# Save the face data dictionary to a file (e.g., pickle or JSON)
import pickle

with open('face_data.pkl', 'wb') as file:
    pickle.dump(face_data, file)

print("Face data saved successfully.")
