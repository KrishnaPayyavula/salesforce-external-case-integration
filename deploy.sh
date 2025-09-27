#!/bin/bash

# Salesforce External Case Integration - Deployment Script

set -e

echo "🚀 Salesforce External Case Integration - Deployment Script"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Parse command line arguments
ENVIRONMENT="development"
BUILD_ARGS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --prod)
            ENVIRONMENT="production"
            shift
            ;;
        --build-args)
            BUILD_ARGS="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --env ENVIRONMENT    Set environment (development|production) [default: development]"
            echo "  --prod               Use production configuration"
            echo "  --build-args ARGS    Additional Docker build arguments"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option $1"
            exit 1
            ;;
    esac
done

print_status "Deploying in $ENVIRONMENT mode"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from env.example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        print_warning "Please update .env file with your actual configuration before proceeding."
        print_warning "Press Enter to continue after updating .env file, or Ctrl+C to exit."
        read
    else
        print_error "env.example file not found. Please create .env file manually."
        exit 1
    fi
fi

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Remove old images (optional)
if [ "$ENVIRONMENT" = "production" ]; then
    print_status "Cleaning up old images..."
    docker system prune -f
fi

# Build and start containers
if [ "$ENVIRONMENT" = "production" ]; then
    print_status "Building production image..."
    if [ -n "$BUILD_ARGS" ]; then
        docker-compose --profile production build $BUILD_ARGS
    else
        docker-compose --profile production build
    fi
    
    print_status "Starting production containers..."
    docker-compose --profile production up -d
else
    print_status "Building development image..."
    if [ -n "$BUILD_ARGS" ]; then
        docker-compose -f docker-compose.dev.yml build $BUILD_ARGS
    else
        docker-compose -f docker-compose.dev.yml build
    fi
    
    print_status "Starting development containers..."
    docker-compose -f docker-compose.dev.yml up -d
fi

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Health check
print_status "Performing health check..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "✅ Health check passed!"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        print_status "Health check attempt $RETRY_COUNT/$MAX_RETRIES failed, retrying in 5 seconds..."
        sleep 5
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    print_error "Health check failed after $MAX_RETRIES attempts"
    print_status "Container logs:"
    docker-compose logs --tail=50
    exit 1
fi

# Show deployment information
print_status "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Information:"
echo "  Environment: $ENVIRONMENT"
echo "  API URL: http://localhost:8000"
echo "  Documentation: http://localhost:8000/docs"
echo "  Health Check: http://localhost:8000/health"
echo ""

if [ "$ENVIRONMENT" = "production" ]; then
    echo "🌐 Production URLs (if nginx is enabled):"
    echo "  API URL: http://localhost"
    echo "  Documentation: http://localhost/docs"
fi

echo ""
echo "📊 Container Status:"
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose --profile production ps
else
    docker-compose -f docker-compose.dev.yml ps
fi

echo ""
echo "📝 Useful Commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop services: docker-compose down"
echo "  Restart services: docker-compose restart"
echo "  Shell access: docker-compose exec salesforce-api bash"
echo ""

print_status "Deployment script completed!"
