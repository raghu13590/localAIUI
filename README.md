# localAIUI

This project is a web-based application that allows users to interact with locally installed Ollama models and also use LangChain to interface with Ollama llms. The application consists of a frontend built with Vue.js and a backend built with Flask. The backend interacts with AI models and provides responses to user queries.

## Prerequisites

- Docker Desktop

## Setup

### Step 1: Clone the Repository

```sh
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Build and Run the Application with Docker Compose

```sh
docker-compose up --build
```

This command will build and start the following services:
- `searxng`: A search engine service.
- `ollama`: The backend service for handling AI queries.
- `frontend`: The frontend service for the web application.

### Step 3: Access the Application

Open your web browser and navigate to `http://localhost:3000` to access the Ollama AI Assistant.

## Usage

1. Select an AI model from the dropdown menu.
2. Choose the query type (`LangChain` or `Direct LLM`).
3. Type your message in the input box and press `Send`.
4. The AI response will be displayed in the chat window.

## Dockerfile and Docker Compose

The project includes Dockerfiles for both the frontend and backend services, as well as a `docker-compose.yml` file to orchestrate the services.

### Frontend Dockerfile

The `frontend/Dockerfile` builds the Vue.js application and serves it using Nginx.

### Backend Dockerfile

The `ollama/Dockerfile` sets up the Flask application and installs the necessary dependencies.

### Docker Compose

The `docker-compose.yml` file defines the services and their configurations, including ports, volumes, and environment variables.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
