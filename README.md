# K2 Communications AI Chatbot

An intelligent AI-powered chatbot designed for **K2 Communications**, India's premier public relations and communications agency. This modern, scalable solution helps clients discover services, handle inquiries, manage crises, and engage with K2's comprehensive PR offerings.

## 🌟 About K2 Communications

K2 Communications (https://www.k2communications.in/) is a leading PR agency in India, serving major brands across multiple sectors with:

- **PR Consultancy**: Strategic public relations and media relations
- **Reputation & Crisis Management**: 24/7 crisis response and reputation monitoring
- **Digital & Social Media Marketing**: Comprehensive digital strategies
- **Content Development**: High-quality content creation
- **Market Research**: In-depth market analysis and insights
- **Translation Services**: Multilingual campaign support across India

### Core Values
- Ethical practices and transparency
- Embracing new technologies including AI
- Multilingual, nationwide coverage
- Excellence in client service

## 🚀 Features

### 1. Floating AI Assistant Widget (NEW!)
- **Attractive Floating Button**: Circular chat icon positioned at bottom-right corner
- **Hover Tooltip**: "I am the K2 AI Assistant, how may I help you?"
- **Popup Chat Window**: ~360px × 720px responsive chat interface
- **Live AI Responses**: Real-time answers powered by OpenAI
- **Modern Design**: Light bluish background, rounded corners, subtle shadows
- **Loading Indicators**: Visual feedback while waiting for responses
- **Error Handling**: Graceful error messages for connection issues
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Static Homepage**: Clean, professional landing page showcasing K2 Communications

### 2. Admin-Managed Q&A System
- **Admin Panel**: Web-based interface at `/admin` to manage Q&A pairs
- **Live Updates**: Add, edit, or delete Q&A pairs without redeployment
- **Priority Answers**: Admin-curated answers take precedence over AI responses
- **Answer Source Indicators**: Clear labels showing if answers are "Admin", "Curated", or "AI Generated"
- **Secure Access**: Password-protected admin interface
- **Persistent Storage**: Q&A pairs stored in JSON file, survive restarts
- **Instructions Panel**: Built-in guidance for using admin features

### 3. Hybrid Q&A System
- **Predefined Q&A**: Fast, consistent answers for common questions
- **LLM Fallback**: AI-powered responses for complex or unique queries
- **Smart Matching**: Keyword-based fuzzy matching with confidence scores
- **Easy Maintenance**: Update Q&A via JSON file without code changes
- See `backend/QA_IMPLEMENTATION.md` for details

### 3. Service Discovery & Lead Capture
- **Conversational explanations of K2's core services**
- **Interactive client intake forms**
- **Instant inquiry capture and routing**
- **Service recommendations based on client needs**

### 4. PR Operations & Crisis Support
- **FAQs for crisis management scenarios**
- **Reputation repair guidance**
- **24/7 crisis communication support**

### 5. Content & Media Workflow
- **AI-assisted press release briefing**
- **Content writing tips and guidance**
- **Blog and article preparation support**

### 6. Multilingual Conversations
- **Support for English and Indian regional languages**
- **Seamless language switching**
- **Cultural adaptation in responses**

### 7. Client Campaign Dashboard (Planned)
- **Campaign progress tracking**
- **Coverage reports**
- **News updates**

### 8. Event & Interaction Scheduling (Planned)
- **Interview booking**
- **Press event scheduling**
- **Automated reminders**

### 9. Feedback Collection
- **Automated feedback gathering**
- **AI sentiment analysis**
- **Service improvement insights**

### 10. Social Media Integration (Planned)
- **Campaign posting assistance**
- **Digital PR support**
- **Social media advisory**

## 🏗️ Architecture

### Technology Stack

**Frontend:**
- **Framework**: Next.js 14 (React 18)
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **API Client**: Axios

**Backend:**
- **Framework**: FastAPI (Python)
- **AI/LLM**: OpenAI GPT-4 (configurable for Azure OpenAI or OSS models)
- **Server**: Uvicorn (ASGI)

**Deployment:**
- **Containerization**: Docker & Docker Compose
- **Platform**: Render for both frontend and backend

### Project Structure

```
k2ai/
├── frontend/                  # Next.js React application
│   ├── src/
│   │   ├── app/              # Next.js app directory
│   │   ├── components/       # React components
│   │   ├── lib/             # API clients and utilities
│   │   ├── styles/          # Global styles
│   │   └── types/           # TypeScript type definitions
│   ├── public/              # Static assets
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                  # FastAPI Python application
│   ├── routes/              # API route handlers
│   ├── services/            # Business logic
│   ├── models/              # Data models
│   ├── utils/               # Utility functions
│   ├── main.py              # Application entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── shared/                   # Shared resources (future)
├── docs/                     # Additional documentation
├── docker-compose.yml        # Multi-container setup
└── README.md                # This file
```

## 🛠️ Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Docker** and Docker Compose (optional)
- **OpenAI API Key** (or Azure OpenAI credentials)

### Installation

#### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/phildass/k2ai.git
cd k2ai
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your OpenAI API key

# Frontend
cp frontend/.env.example frontend/.env.local
```

3. **Start with Docker Compose**
```bash
docker-compose up --build
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

#### Option 2: Manual Setup

**Backend Setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# Run the server
uvicorn main:app --reload --port 8000
```

**Frontend Setup:**

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local if needed

# Run development server
npm run dev
```

### Environment Configuration

> **⚠️ IMPORTANT:** For detailed OpenAI API setup instructions, see **[OPENAI_SETUP_GUIDE.md](OPENAI_SETUP_GUIDE.md)**

**Backend (.env):**
```env
OPENAI_API_KEY=your_openai_api_key_here  # Get from https://platform.openai.com/api-keys
ADMIN_PASSWORD=k2admin2026  # Change this to a secure password for production
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Verify Your Setup

After configuration, verify your OpenAI integration:

```bash
cd backend
python test_openai_connection.py
```

Expected output:
```
✓ OpenAI API key is configured
✓ Successfully connected to OpenAI API
✓ Live AI assistant is working!
```

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## 📊 Admin Panel

The admin panel allows authorized users to manage Q&A pairs that take priority over AI-generated responses.

### Access the Admin Panel

1. **Navigate to** `http://localhost:3000/admin` (or your deployed URL + `/admin`)
   - You can also click "Admin" in the navigation menu on the homepage
2. **Login with password**: Default is `k2admin2026` (set via `ADMIN_PASSWORD` environment variable)
3. **Manage Q&A pairs**: Add, edit, or delete custom responses

### Admin Panel Features

- **Add Q&A Pairs**: Create new question-answer pairs that the AI will use
- **Edit Existing Pairs**: Update questions or answers as needed
- **Delete Pairs**: Remove outdated or incorrect Q&A pairs
- **Live Updates**: Changes take effect immediately without restarting the server
- **Persistent Storage**: All Q&A pairs are stored in `backend/data/admin_qa.json`
- **Instructions Panel**: Clear guidance on how to use the admin features

### How It Works

The admin panel provides a user-friendly interface to:
- Manage custom responses for frequently asked questions
- Override AI-generated answers with curated content
- Ensure consistent, accurate responses for important queries
- Update content without code changes or server restarts

The system uses fuzzy matching, so questions don't need to match exactly - similar questions will also trigger your custom answers.

### Answer Priority

When a user asks a question, the system checks answers in this order:
1. **Admin Q&A** (highest priority) - Manually curated answers from `/admin`
2. **FAQ Answers** - Private FAQ entries in `backend/private_faq/faqs.json`
3. **Predefined Q&A** - Public Q&A in `backend/data/predefined_qa.json`
4. **AI Generated** (lowest priority) - OpenAI API for unknown queries

### Answer Source Indicators

The chat interface displays badges showing the source of each answer:
- 🟢 **Admin Answer** - From admin panel
- 🔵 **Curated Answer** - From FAQ or predefined Q&A
- 🟣 **AI Generated** - From OpenAI API

### Security Notes

⚠️ **Important for Production:**
- **Change the default password**: Set a strong, unique password in your `.env` file
- The default password is `k2admin2026` - DO NOT use this in production
- Use a strong, unique password (e.g., `MySecureP@ssw0rd2026!`)
- Set `ADMIN_PASSWORD` in your `backend/.env` file
- Consider implementing proper authentication (OAuth, JWT) for production use
- The current implementation is a simple token-based auth suitable for internal use
- Admin tokens are stored in browser localStorage and persist across sessions

## 📖 API Documentation

### Chat Endpoints

**POST /api/chat/** or **POST /api/chat/message**
- Send a message to the AI chatbot
- Supports predefined Q&A with LLM fallback
- Supports multilingual conversations
- Returns AI response with suggestions and metadata
- Response includes `answer_source` field: "admin", "faq", "predefined", or "ai"

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?", "conversation_id": "test-123"}'
```

**Example Response:**
```json
{
  "message": "K2 Communications offers comprehensive PR and communications services...",
  "conversation_id": "test-123",
  "suggestions": ["Tell me more about PR consultancy", "What is crisis management?"],
  "answer_source": "predefined",
  "metadata": {
    "source": "predefined",
    "matched_question": "What services do you offer?",
    "confidence": 1.0,
    "language": "en",
    "timestamp": "2026-01-14T08:00:00.000000"
  }
}
```

**Run the example script:**
```bash
cd backend
python example_api_usage.py
```

See `backend/QA_IMPLEMENTATION.md` for detailed information about the Q&A system.

**GET /api/chat/conversation/{conversation_id}**
- Retrieve conversation history

### Service Endpoints

**GET /api/services/**
- Get all K2 Communications services

**GET /api/services/{service_id}**
- Get specific service details

### Feedback Endpoints

**POST /api/feedback/submit**
- Submit user feedback

**POST /api/feedback/lead**
- Capture lead information

Full interactive API documentation available at: http://localhost:8000/docs

## 🎨 Customization

### Branding
Update brand colors, logos, and styling in:
- `frontend/tailwind.config.js` - Color scheme
- `frontend/src/app/layout.tsx` - Site metadata
- `frontend/public/` - Add logo and favicon

### AI Behavior
Customize the chatbot's personality and knowledge:
- `backend/services/chatbot_service.py` - System prompts
- `backend/routes/services.py` - Service information

### Services Data
Update K2's services in:
- `backend/routes/services.py` - K2_SERVICES array

## 🔒 Security Considerations

- Never commit `.env` files with real API keys
- Use environment variables for all sensitive data
- Implement rate limiting in production
- Add authentication for admin features
- Validate and sanitize all user inputs
- Use HTTPS in production

## 🚢 Deployment

### Render Deployment

The repository is deployed to Render for both frontend and backend services.

**Prerequisites:**
- GitHub account connected to Render
- OpenAI API key from https://platform.openai.com/api-keys

**Deployment Steps:**

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

**Quick Overview:**

1. **Backend Deployment**
   - Create a new Web Service on Render
   - Connect your GitHub repository: `phildass/k2ai`
   - Set root directory to `backend`
   - Configure runtime: Python 3
   - Set environment variables (OPENAI_API_KEY, etc.)
   - Deploy

2. **Frontend Deployment**
   - Create a new Web Service on Render
   - Connect your GitHub repository: `phildass/k2ai`
   - Set root directory to `frontend`
   - Configure runtime: Node
   - Set environment variables (NEXT_PUBLIC_API_URL)
   - Deploy

3. **Custom Domain (Optional)**
   - Configure custom domain in Render settings
   - Update DNS records with your DNS provider

**Important Notes:**
- Never commit `.env` files with real API keys to GitHub
- The server automatically uses `process.env.PORT` provided by Render
- Render free tier apps may spin down after inactivity - first request might be slow
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions


## 🧪 Testing

**Backend:**
```bash
cd backend
pytest  # (tests to be added)
```

**Frontend:**
```bash
cd frontend
npm run test  # (tests to be added)
```

## 📈 Future Enhancements

- [ ] User authentication and session management
- [ ] Database integration for conversation history
- [ ] WhatsApp/Slack bot integration
- [ ] Advanced analytics dashboard
- [ ] Multi-model LLM support (Llama, Claude, etc.)
- [ ] Voice input/output capabilities
- [ ] Calendar integration for scheduling
- [ ] CRM integration
- [ ] Enhanced multilingual support with translation APIs
- [ ] A/B testing for chatbot responses

## 🤝 Contributing

This is an internal project for K2 Communications. For team members:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Proprietary - K2 Communications. All rights reserved.

## 📞 Support

For support and questions:
- **Internal Team**: Contact the development team
- **K2 Communications**: Visit https://www.k2communications.in/

## 🙏 Acknowledgments

Built for K2 Communications with cutting-edge AI technology to enhance client engagement and streamline PR operations.

---

**Powered by OpenAI GPT-4 | Built with Next.js & FastAPI**