# SVG Repository API 🚀  
This API converts SVG containing Web Image Links to PNG files.  

---

## **📌 Endpoints**  

### **🔹 POST `/convert-svg`**  
Converts SVG code (containing Web Image Links or not) to PNG and SVG files.  

#### **📌 Request**  

🔹 **Headers:**  
```
Content-Type: application/json  
X-API-KEY: {your_secret_key}
```

🔹 **Body (Raw JSON):**  
```json
{
    "svg_content": "<svg ... svg>",
    "output_folder": "output_svgs"
}
```

---

## **📌 Response**  

### **🟩 Success (`200 OK`)**  
```json
{
  "message": "SVGs successfully converted!",
  "files": [
    {
      "svg_download": "/download/converted-file.svg",
      "png_download": "/download/converted-file.png"
    }
  ]
}
```

### **🔴 Error (`400 Bad Request`)**  
```json
{ "error": "SVG content is required!" }
```

### **🔴 Error (`403 Forbidden`)**  
```json
{ "error": "Invalid API key" }
```

---

## **📌 Endpoints**  

### **🔹 GET `/download/{filename}`**  
Download PNG or SVG file.  

📌 **Example usage:**  
```
GET https://your-domain.com/download/converted_image.png
```

📌 **Response:**  
- Returns the requested file for download.  

📌 **Error (`404 Not Found` - File not found):**  
```json
{ "error": "File not found" }
```

---

## **📌 Authentication & Security**  
✅ **API Key Authentication:** All requests must include the `X-API-KEY` header.  
✅ **Rate Limit:** Maximum **5 requests per minute per IP**.  

---

## **📌 How to Run Locally**  

### 📌 **Prerequisites:**  
- Python 3.x  
- Install dependencies:  
```bash
pip install -r requirements.txt
```

### 📌 **Run the API:**  
```bash
python app.py
```

### 📌 **Deploy on Fly.io:**  
```bash
fly deploy
```