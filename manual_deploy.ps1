# Manual deployment script for Cloud Run (PowerShell version)
# Run this if automatic deployment fails

Write-Host "🤖 Manual Cloud Run Deployment Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Set variables
$PROJECT_ID = "gen-lang-client-0502058841"
$SERVICE_NAME = "devops-backup"
$REGION = "europe-west1"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
docker build -t $IMAGE_NAME .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker build successful!" -ForegroundColor Green
    
    Write-Host "📤 Pushing to Google Container Registry..." -ForegroundColor Yellow
    docker push $IMAGE_NAME
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Image pushed successfully!" -ForegroundColor Green
        
        Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Yellow
        gcloud run deploy $SERVICE_NAME `
            --image $IMAGE_NAME `
            --platform managed `
            --region $REGION `
            --allow-unauthenticated `
            --port 8080 `
            --memory 1Gi `
            --cpu 1 `
            --max-instances 10 `
            --min-instances 0 `
            --timeout 300 `
            --project $PROJECT_ID
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Deployment successful!" -ForegroundColor Green
            Write-Host "🌐 Your app should be available at:" -ForegroundColor Cyan
            gcloud run services describe $SERVICE_NAME --region $REGION --project $PROJECT_ID --format="value(status.url)"
        } else {
            Write-Host "❌ Deployment failed!" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "❌ Image push failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}