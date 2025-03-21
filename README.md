# ⛏️ Minecraft Character Generator

A web application that generates Minecraft-style character images based on text descriptions using Azure OpenAI's DALL-E 3 model. The app also generates QR codes for easy sharing and downloads images to Azure Blob Storage.

## 📋 Features

- Generate Minecraft style character images from text descriptions
- Automatic image storage in Azure Blob Storage
- QR code generation for easy sharing
- Simple, user-friendly Streamlit interface

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Azure OpenAI account with DALL-E 3 access
- Azure Storage account

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd oai-funko-generator
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.sample` to `.env`
   - Fill in your Azure OpenAI and Azure Storage credentials

### Configuration

Update the `.env` file with your credentials:
```
MODEL_DALLE="dall-e-3"
DEPLOYMENT_NAME_DALLE=dall-e-3
ENDPOINT_DALLE=your-azure-openai-endpoint
API_KEY_DALLE=your-api-key
API_TYPE_DALLE=openai
API_VERSION_DALLE=2024-10-21

AZURE_STORAGE_CONNECTION_STRING=your-azure-storage-connection-string
```

## 🖥️ Running the Application

Start the Streamlit app:
```
streamlit run app.py
```

Then navigate to the provided URL (typically http://localhost:8501) in your web browser.
