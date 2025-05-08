# Deployment Options for Twitter AI Assistant

## Option 1: Digital Ocean or AWS EC2

This is the recommended option to run the full application with Twitter scraping.

1. Create a Digital Ocean Droplet or AWS EC2 instance (Ubuntu 20.04 LTS recommended)
2. SSH into your server
3. Install Docker and Docker Compose
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   ```
4. Clone your repository
   ```bash
   git clone https://github.com/yourusername/twitter-ai-assistant.git
   cd twitter-ai-assistant
   ```
5. Create a .env file with your OpenAI API key
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```
6. Build and run with Docker Compose
   ```bash
   docker-compose up -d
   ```
7. Access the app at http://your-server-ip:8501

## Option 2: Railway.app

Railway.app supports Docker deployments and has a generous free tier.

1. Install the Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Create a new project: `railway init`
4. Add your OpenAI API key as a variable in the Railway dashboard
5. Deploy: `railway up`

## Option 3: Render.com

Render supports Docker deployments and has a free tier.

1. Create a new Web Service in Render
2. Connect your GitHub repository
3. Select "Docker" as the environment
4. Add your OpenAI API key as an environment variable
5. Deploy

## For All Deployment Options

Important notes:

1. The Twitter scraping feature requires a browser, which is included in the Docker setup
2. You'll need an OpenAI API key to use the AI question answering feature
3. For long-term use, consider setting up a proper login system
