#!/bin/bash

# Smart Documentation Agent - Setup Script
# This script helps you set up the project on a new machine

echo "🚀 Setting up Smart Documentation Agent..."
echo ""

# Check if .env exists
if [ -f "backend/.env" ]; then
    echo "⚠️  backend/.env already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

# Copy .env.example to .env
cp backend/.env.example backend/.env
echo "✅ Created backend/.env from template"

# Prompt for API keys
echo ""
echo "📝 Please enter your API keys:"
echo ""

# Get Gemini API key
read -p "Enter your Gemini API Key (get from https://aistudio.google.com/apikey): " GEMINI_KEY

# Get GitHub token (optional)
echo ""
echo "GitHub Personal Access Token is optional (press Enter to skip)"
read -p "Enter your GitHub Token (optional, for higher rate limits): " GITHUB_TOKEN

# Update .env file
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    sed -i '' "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_KEY/" backend/.env
    if [ ! -z "$GITHUB_TOKEN" ]; then
        sed -i '' "s/GITHUB_TOKEN=.*/GITHUB_TOKEN=$GITHUB_TOKEN/" backend/.env
    fi
else
    # Linux
    sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_KEY/" backend/.env
    if [ ! -z "$GITHUB_TOKEN" ]; then
        sed -i "s/GITHUB_TOKEN=.*/GITHUB_TOKEN=$GITHUB_TOKEN/" backend/.env
    fi
fi

echo ""
echo "✅ API keys configured!"
echo ""

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✨ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser!"
echo ""
