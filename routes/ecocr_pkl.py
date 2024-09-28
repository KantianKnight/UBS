import easyocr
import pickle

# Create the EasyOCR Reader object
reader = easyocr.Reader(['en'])

# Save the Reader object to a file
with open('easyocr_reader.pkl', 'wb') as f:
    pickle.dump(reader, f)