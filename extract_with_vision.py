import os
from google.cloud import vision
from pdf2image import convert_from_path
import base64
from pathlib import Path

def extract_with_google_vision(pdf_path, api_key):
    """Extract text from image PDFs using Google Cloud Vision"""
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=200)
        text = ""
        
        # For each page, extract text using Google Vision
        for image in images:
            # Convert image to bytes
            import io
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_content = base64.b64encode(buffered.getvalue()).decode()
            
            # Call Google Vision API
            client = vision.ImageAnnotatorClient()
            image = vision.Image(content=base64.b64decode(image_content))
            response = client.text_detection(image=image)
            
            # Extract text
            if response.text_annotations:
                text += response.text_annotations[0].description
        
        return text if text.strip() else None
    except Exception as e:
        return None

def process_all_resumes_with_vision():
    """Process all resumes using Google Vision"""
    input_folder = r"C:\Users\HP\Desktop\Rag Resume Analyzer\resumes_to_validate"
    output_folder = "./extracted_resumes"
    
    Path(output_folder).mkdir(exist_ok=True)
    
    files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]
    
    print("=" * 80)
    print(f"EXTRACTING {len(files)} RESUMES WITH GOOGLE VISION")
    print("=" * 80)
    
    extracted_count = 0
    
    for file in sorted(files):
        file_path = os.path.join(input_folder, file)
        
        # Try Google Vision
        print(f"⏳ {file} (using Google Vision...)")
        text = extract_with_google_vision(file_path, os.getenv("GOOGLE_API_KEY"))
        
        if text:
            txt_name = file.replace('.pdf', '.txt')
            txt_path = os.path.join(output_folder, txt_name)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✅ {file}")
            extracted_count += 1
        else:
            print(f"❌ {file} (extraction failed)")
    
    print("=" * 80)
    print(f"Successfully extracted: {extracted_count}/{len(files)}")
    print("=" * 80)

if __name__ == "__main__":
    process_all_resumes_with_vision()