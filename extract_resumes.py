import os
import pypdf
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file (text-based)"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        return text if text.strip() else None
    except Exception as e:
        return None

def extract_text_from_image_pdf(pdf_path):
    """Extract text from image-based PDF using OCR"""
    try:
        from pdf2image import convert_from_path
        import pytesseract
        
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        text = ""
        
        # Extract text from each image
        for image in images:
            try:
                text += pytesseract.image_to_string(image)
            except:
                pass
        
        return text if text.strip() else None
    except:
        return None

def process_all_resumes():
    """Process all resumes with fallback to OCR"""
    
    input_folder = r"C:\Users\HP\Desktop\Rag Resume Analyzer\resumes_to_validate"
    output_folder = "./extracted_resumes"
    
    Path(output_folder).mkdir(exist_ok=True)
    
    # Get all PDF files
    files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]
    
    print("=" * 80)
    print(f"EXTRACTING {len(files)} RESUMES")
    print("=" * 80)
    
    extracted_count = 0
    
    for file in sorted(files):
        file_path = os.path.join(input_folder, file)
        text = ""
        
        # Try text extraction first (fast)
        text = extract_text_from_pdf(file_path)
        
        # If no text, try OCR (slower but handles images)
        if not text:
            print(f"⏳ {file} (using OCR...)")
            text = extract_text_from_image_pdf(file_path)
        
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
    print(f"Location: {output_folder}/")
    print("=" * 80)

if __name__ == "__main__":
    process_all_resumes()