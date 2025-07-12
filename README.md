# 🛒 Kiryana Stock Agent# Kirana Store Reorder Assistant

A web application that helps Pakistani kirana store owners manage their inventory by processing handwritten sales register images and suggesting reorders.

## Features

- Upload handwritten sales register images in Urdu or English
- Automatic item and quantity extraction using OCR
- Smart reorder suggestions based on stock levels
- WhatsApp notifications for reorder suggestions
- Clean and intuitive web interface

## Setup Instructions
**Kiryana Stock Agent** solves this by:

- 📷 Allowing store owners to upload a photo of their register
- 🤖 Using OCR to extract items and quantities
- 📦 Generating reorder suggestions automatically
- 📲 Delivering the results via a web dashboard or WhatsApp message

Built at **Hackfest 2025** to demonstrate how domain-specific AI can solve everyday retail inefficiencies in Pakistan.

---

## 🧠 Features

- 🧾 OCR-powered data extraction (Urdu + English)
- 📊 Smart reorder suggestion engine
- 🖥️ Simple web interface for photo uploads and results
- 📬 WhatsApp integration (Twilio Sandbox demo)
- ✅ Fast, low-friction MVP experience

---

## 📸 Demo

| Upload Interface         | Results Table            | WhatsApp Output         |
|--------------------------|---------------------------|--------------------------|
| ![Upload](assets/upload.png) | ![Result](assets/result.png) | ![WhatsApp](assets/whatsapp.png) |

> *(Replace the `assets/` image links with your actual screenshot paths)*

---

## 🚀 How It Works

1. Shopkeeper uploads a register image
2. OCR engine extracts item names and quantities
3. AI logic decides what to reorder
4. Results shown on dashboard and optionally sent on WhatsApp

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit / HTML + Tailwind CSS
- **Backend**: Flask / FastAPI (Python)
- **OCR**: Google Vision API / PaddleOCR
- **Messaging**: Twilio WhatsApp Sandbox
- **Hosting**: Render / Railway / Replit

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/kiryana-stock-agent.git
cd kiryana-stock-agent

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
