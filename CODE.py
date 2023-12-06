import cv2
import boto3
import pyttsx3
import face_recognition
    
# AWS credentials and region
aws_access_key_id = 'AKIAVN3OW3HF2MV52PHW'
aws_secret_access_key = 'U8ttMSJcSYEUZ8Wa9UkekZUNJu4bfMCnSvJ9I/Oo'
region_name = 'ap-south-1'
bucket_name = 'pythonaatproject'  # Update with your S3 bucket name

# Create an S3 client
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Create a Rekognition client
rekognition_client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Function to capture driver's face
def capture_face():
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("Failed to open the camera")
        return

    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        cv2.imshow("driver's Face", frame)  # Display the frame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save the captured face image
    cv2.imwrite('image_path', frame)

# Function to upload reference images to S3
object_key = 'reference_image.jpg'
image_path = r'C:\\Users\\subra\\Downloads\\reference_image.jpg'

def upload_reference_image(image_path, object_key):
    with open(image_path, 'rb') as image_file:
        s3_client.upload_fileobj(image_file, bucket_name, object_key)

# Function to perform face recognition with Rekognition
def perform_face_recognition():
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Call Amazon Rekognition's detect_faces API
    response = rekognition_client.detect_faces(Image={'Bytes': image_data})

    if len(response['FaceDetails']) > 0:
        # Extract the driver's face details
        face_detail = response['FaceDetails'][0]
        reference_image = face_recognition.load_image_file(image_path)

        # Encode the reference image
        reference_encoding = face_recognition.face_encodings(reference_image)[0]

        # Encode the captured face
        captured_image = face_recognition.load_image_file('driver_face.jpg')
        captured_encoding = face_recognition.face_encodings(captured_image)

        if len(captured_encoding) > 0:
            captured_encoding = captured_encoding[0]

        # Compare the encodings
        results = face_recognition.compare_faces([reference_encoding], captured_encoding)

        if results[0]:
            # Get the driver's name
            driver_name = 'musk'  # Replace with the actual driver's name

            # Display the driver's name
            print("Driver identified:", driver_name)

            # Generate voice alert to welcome the driver
            welcome_message = f"Welcome, {driver_name}! Have a great day!"
            engine.say(welcome_message)
            engine.runAndWait()

        else:
            print("No driver face detected")

    else:
        print("No face detected in the captured image")

# Main function to execute the project
def main():
    # Step 1: Capture the driver's face
    capture_face()
# Step 2: Upload reference images to S3 (if needed)
 #upload_reference_image(r"C:\Users\subra\Downloads\reference_image.jpg") # Uncomment this line

 # Step 3: Perform face recognition using Amazon Rekognition
perform_face_recognition()
main()
