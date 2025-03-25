# ⛏️ Minecraft Character Generator

A web application that generates Minecraft-style character images based on text descriptions or webcam photos using Azure AI services. The app uses DALL-E 3 for image generation and Mistral for facial analysis, with automatic image storage to Azure Blob Storage and QR code generation for easy sharing.

## 📋 Features

- Generate Minecraft style character images from text descriptions
- Analyze facial features from webcam photos to generate personalized characters
- Automatic image storage in Azure Blob Storage
- QR code generation for easy sharing
- Simple, user-friendly Streamlit interface

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Azure OpenAI account with DALL-E 3 access
- Azure AI Services account with Mistral model access
- Azure Storage account

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd oai-minecraft-generator
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.sample` to `.env`
   - Fill in your Azure OpenAI, Azure AI, and Azure Storage credentials

### Configuration

Update the `.env` file with your credentials:
```
# DALL-E Configuration
MODEL_DALLE="dall-e-3"
DEPLOYMENT_NAME_DALLE=dall-e-3
ENDPOINT_DALLE=your-azure-openai-endpoint
API_KEY_DALLE=your-api-key
API_TYPE_DALLE=openai
API_VERSION_DALLE=2024-10-21

# Mistral Configuration
MODEL_MISTRAL="Mistral Small"
DEPLOYMENT_NAME_MISTRAL=your-mistral-deployment
ENDPOINT_MISTRAL=your-mistral-endpoint
API_KEY_MISTRAL=your-mistral-api-key
API_TYPE_MISTRAL=azure
API_VERSION_MISTRAL=2024-05-01-preview

# Azure Blob Storage Configuration
AZURE_STORAGE_CONNECTION_STRING=your-azure-storage-connection-string
```

## 🖥️ Running the Application

Start the Streamlit app:
```
streamlit run app.py
```

Then navigate to the provided URL (typically http://localhost:8501) in your web browser.
