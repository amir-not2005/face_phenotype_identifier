import face_recognition
import os
import matplotlib.pyplot as plt
from PIL import Image

# Start
print('Turning on the program')


# Data
def load_images():
    known_encodings = []
    names = []
    for filename in os.listdir("images"):
        print(filename)
        known_image = face_recognition.load_image_file("images/"+filename)
        face_encoding = face_recognition.face_encodings(known_image)[0]
        known_encodings.append(face_encoding)
        names.append(filename[0:-4])
    print("Found", len(os.listdir("images")), "images")
    return known_encodings, names
    
# Program
def compare_faces(known_encodings, names):
    
    #Your picked photo
    print('Loading the photo')

    # Load a test image and get encondings for it
    your_photo = input("Write name of the file: ")
    image_to_test = face_recognition.load_image_file(your_photo)
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]


    #Calculating
    print("Calculating...")
    print()

    # See how far apart the test image is from the known faces
    face_distances = face_recognition.face_distance(known_encodings,image_to_test_encoding)
    result_distance = 1.0
    result_name = ""
    for i, face_distance in enumerate(face_distances):
        print("The test image has a distance of {:.2} from known image {}".format(face_distance, names[i]))
        if (face_distance < result_distance):
            result_distance = face_distance
            result_name = names[i]
    print("\nThe closest race is: ", str(result_distance), result_name)
    return your_photo, result_name

# Visual
def demonstrate_photos(user_image, result_image):
    user_img = Image.open(user_image) 
    result_img = Image.open("images/"+result_image+".jpg")

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns

    # First image
    axes[0].imshow(user_img)
    axes[0].axis('off')  # Hide the axes
    axes[0].set_title('Your image')  # Set title for the first image

    # Second image
    axes[1].imshow(result_img)
    axes[1].axis('off')  # Hide the axes
    axes[1].set_title(result_image)  # Set title for the second image

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()


known_encodings, names = load_images()
your_photo, result_image = compare_faces(known_encodings, names)
demonstrate_photos(your_photo, result_image)
