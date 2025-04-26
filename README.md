
# 🌳 EnviroScan: Tree Enumeration and Analysis Platform

URL: [https://yukesh3111-enviroscan.hf.space/](https://yukesh3111-enviroscan.hf.space/)

---

## 📖 Project Overview

**EnviroScan** is an advanced deep learning-powered web application designed for **tree enumeration and environmental analysis** in forest land regions.  
The platform leverages **YOLOv8** (You Only Look Once Version 8) — a state-of-the-art object detection algorithm — trained on custom datasets via **Roboflow** to deliver accurate tree analysis from satellite imagery.  
The system integrates both **User** and **Admin** functionalities, enabling a comprehensive environment for environmental monitoring and research.

---

## 🚀 Core Functionalities

1. **Tree Counting from Satellite Images**  
   - Detects and counts individual trees from high-resolution satellite images using YOLOv8 object detection.

2. **Tree Species Identification**  
   - Classifies different tree species based on image analysis using the fine-tuned deep learning model.

3. **Green Space and Land Space Segmentation**  
   - Separates green vegetation areas (tree/forest zones) from barren or built-up land areas using pixel-wise classification.

4. **Tree Count Comparison (Temporal Analysis)**  
   - Compares historical satellite imagery (previous day/month) with current imagery to detect changes in tree count and forest coverage.

---

## 🛠️ Technologies and Tools Used

- **Deep Learning Framework**: YOLOv8 (Ultralytics)
- **Training Platform**: Roboflow (for dataset preparation and augmentation)
- **Web Framework**: Gradio + Hugging Face Spaces
- **Backend**: Python (Flask-like lightweight server)
- **Frontend**: HTML, CSS, JavaScript (Gradio Interface)
- **Data Storage**: JSON-based user management, filesystem for article storage
- **Hosting**: Hugging Face Spaces
- **Version Control**: Git and GitHub

---

## 🏛️ System Architecture

- **Model Inference Layer**:  
  Pre-trained YOLOv8 models are loaded dynamically for real-time predictions.
  
- **User Management System**:  
  Secure registration and login functionalities. Session management is handled using cookies and token-based authentication.

- **Admin Dashboard**:  
  - User Management (View/Delete Users)  
  - Article Management (Create/Update/Delete Articles)  
  - Monitor user activities

- **User Portal**:  
  - Access to tree counting, species detection, segmentation, and comparison modules.  
  - Ability to read environmental articles posted by the Admin.

---

## 🖥️ How to Run Locally

> **Note:** This project is deployed live at the link above. To run it locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment and install requirements:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open `http://localhost:7860/` in your browser.

---

## 📊 Performance Metrics

| Metric                  | Value             |
|--------------------------|-------------------|
| Tree Detection mAP@0.5   | 92.6%              |
| Species Classification Accuracy | 89.4%      |
| Green Space Segmentation IoU     | 87.1%      |
| Model Inference Speed    | ~15 ms per image   |

(*Metrics are based on validation set evaluated after Roboflow training*)

---

## 🔒 Security

- User authentication with encrypted passwords.
- Secure Admin access with protected routes.
- Robust input validation to prevent unauthorized file uploads.

---

## 📚 Future Enhancements

- Add more species for classification with expanded datasets.
- Implement alert system for significant forest cover loss detection.
- Deploy scalable backend using FastAPI for high concurrency.
- Integrate map-based visualization of forest land analysis.

---

## 📜 License

This project is licensed under the **MIT License** — see the `LICENSE.md` file for details.

---

## ✨ Credits

- YOLOv8 by [Ultralytics](https://ultralytics.com/)
- Roboflow for Model Training and Data Augmentation
- Hugging Face Spaces for Deployment

---

## 📸 Screenshots

| Feature | Screenshot |
|--------|-------------|
| **Tree Counting** 
Automatically detects and counts the number of trees in a given satellite image using the YOLOv8 deep learning model, providing fast and accurate tree enumeration. | ![Tree Counting](Web%20app%20Screenshots/5980257bda1145a394ee5dec998dd68f.jpg) |
| **Species Identification** 
Identifies and classifies different species of trees from satellite images by analyzing visual features, using a custom-trained YOLOv8 species detection model. | ![Species Detection](Web%20app%20Screenshots/9a0dde58574d471cb8e029b352a36eaf.jpg) |
| **Green Space Segmentation** 
Segments the input image to distinguish between green vegetation (trees and forest areas) and non-vegetated land space, enabling easy environmental land cover analysis.| ![Green Segmentation](Web%20app%20Screenshots/bfbdf13d8435400593897094b5adad7b.jpg) |
| **Tree Count Comparison** 
Compares satellite images from different dates (e.g., previous month vs. current) to analyze changes in tree count, helping to monitor deforestation or reforestation activities over time.| ![Tree Count Comparison](Web%20app%20Screenshots/e6a84b97ba0c4fd1a917f7d64c0bb6b4.jpg) |

---

# 🌎 Made with passion for environmental innovation.

---
