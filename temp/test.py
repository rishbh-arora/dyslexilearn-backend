import cv2
from PIL import Image
import pytesseract
# Path to the image file
image_path = "/home/rishab/Desktop/lunux/Code/repos/dyslexilearn/temp/drawing_1NSkpZ1.jpg"  # Replace with your actual image path

# Read the image
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
cv2.imshow('img', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

processed_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                    cv2.THRESH_BINARY, 11, 2)
cv2.imshow('img', processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

pil_image = Image.fromarray(processed_image)
extracted_text = pytesseract.image_to_string(pil_image).strip().lower()
print(extracted_text)