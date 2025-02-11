"""
Digital Image Processing - Simulated Fastag System
"""

import cv2
import numpy as np

# --- Configuration ---
IMAGE_PATH = "fastag_image.png"  # Replace with the path to your image
TAG_ID_REGION = (100, 50, 300, 80)  # (x, y, width, height) of the Tag ID region in the image
TAG_ACCOUNTS = {
    "FASTAG1": 50.0,
    "FASTAG2": 75.0,
    "FASTAG3": 100.0
}

# --- Image Processing Functions ---
def preprocess_image(image):
    """Applies basic image preprocessing.

    Args:
        image: The input image (NumPy array).

    Returns:
        The preprocessed image (NumPy array).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]  # Thresholding
    return thresh


def extract_tag_id(image, region):
    """Simulates Tag ID extraction from a region of interest.

    This is a placeholder.  In a real system, you'd use OCR.

    Args:
        image: The image (NumPy array).
        region: A tuple (x, y, width, height) defining the region of interest.

    Returns:
        A string representing the "extracted" Tag ID (based on a simple lookup).  Returns "UNKNOWN" if extraction fails
    """
    x, y, w, h = region
    roi = image[y:y + h, x:x + w]  # Region of Interest
    # A highly simplified approach
    # We check the average pixel value, and "guess" the Tag ID based on that
    avg_pixel_value = np.mean(roi)

    if avg_pixel_value > 150:
        return "FASTAG1"
    elif avg_pixel_value > 80:
        return "FASTAG2"
    else:
        return "FASTAG3" #Defaulting to FASTAG3 if the average is very low

# --- Transaction Processing Functions (Same as before) ---
def process_transaction_with_error_handling(tag_id, toll_amount, accounts):
    try:
        toll_amount = float(toll_amount)
        if tag_id in accounts:
            if accounts[tag_id] >= toll_amount:
                accounts[tag_id] -= toll_amount
                return accounts[tag_id], "Success"
            else:
                return None, "Insufficient Balance"
        else:
            return None, "Invalid Tag ID"
    except ValueError:
        return None, "Invalid Toll Amount"


# --- Main Program ---
if __name__ == "__main__":
    print("Digital Image Processing - Fastag Simulation")
    print("-------------------------------------------")

    # 1. Load Image
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print(f"Error: Could not load image from {IMAGE_PATH}")
        exit()  # Stop the program if the image can't be loaded

    # 2. Preprocess Image
    preprocessed_image = preprocess_image(image)

    # 3. Extract Tag ID
    extracted_tag_id = extract_tag_id(preprocessed_image, TAG_ID_REGION)
    print(f"Extracted Tag ID: {extracted_tag_id}")

    # 4. Simulate Transaction
    if extracted_tag_id != "UNKNOWN":
      toll = input("Enter Toll Amount: ")  # Get toll amount from user
      new_balance, status = process_transaction_with_error_handling(extracted_tag_id, toll, TAG_ACCOUNTS)

      if status == "Success":
          print("Transaction successful. New balance:", new_balance)
      else:
          print("Transaction failed:", status)

      print("Updated Account Balances:", TAG_ACCOUNTS)
    else:
      print("Could not extract tag ID")
    # 5. Display Results (Optional)
    #  You can display the original and preprocessed images using cv2.imshow()
    #  This is helpful for debugging and visualizing the image processing steps.
    cv2.imshow("Original Image", image)
    cv2.imshow("Preprocessed Image", preprocessed_image)
    cv2.waitKey(0)  # Wait for a key press to close the windows
    cv2.destroyAllWindows()