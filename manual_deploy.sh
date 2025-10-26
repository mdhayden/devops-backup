#!/bin/bash
# Manual deployment script for Cloud Run
# Run this if automatic deployment fails

echo "🤖 Manual Cloud Run Deployment Script"
echo "======================================"

# Set variables
PROJECT_ID="gen-lang-client-0502058841"
SERVICE_NAME="devops-backup"
REGION="europe-west1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful!"
    
    echo "📤 Pushing to Google Container Registry..."
    docker push $IMAGE_NAME
    
    if [ $? -eq 0 ]; then
        echo "✅ Image pushed successfully!"
        
        echo "🚀 Deploying to Cloud Run..."
        gcloud run deploy $SERVICE_NAME \
            --image $IMAGE_NAME \
            --platform managed \
            --region $REGION \
            --allow-unauthenticated \
            --port 8080 \
            --memory 1Gi \
            --cpu 1 \
            --max-instances 10 \
            --min-instances 0 \
            --timeout 300 \
            --project $PROJECT_ID
        
        if [ $? -eq 0 ]; then
            echo "✅ Deployment successful!"
            echo "🌐 Your app should be available at:"
            gcloud run services describe $SERVICE_NAME --region $REGION --project $PROJECT_ID --format="value(status.url)"
        else
            echo "❌ Deployment failed!"
            exit 1
        fi
    else
        echo "❌ Image push failed!"
        exit 1
    fi
else
    echo "❌ Docker build failed!"
    exit 1
fi