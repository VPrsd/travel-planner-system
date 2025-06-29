# Multi-Agent Travel Planning System

A sophisticated travel planning system that uses multiple AI agents to create personalized itineraries.

## 🎯 Features
- **Research Agent (GPT-4)**: Gathers real-time destination data
- **Planning Agent (Claude)**: Optimizes routes, timing, and logistics  
- **Personalization Agent (Gemini)**: Customizes based on preferences
- **Orchestrator**: Coordinates all agents and manages workflow

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API keys for OpenAI, Anthropic, and Google

### Installation
```bash
pip install -r requirements.txt
```

### Setup
1. Copy `.env.example` to `.env`
2. Add your API keys
3. Run the system:
```bash
python src/travel_planner.py --destination "Georgia" --budget 1500 --days 7 --travelers 2 --preferences culture food hiking wine
```

## 📁 Project Structure
```
travel-planner-system/
├── src/                    # Source code
│   ├── agents/            # AI agent implementations
│   ├── utils/             # Utility functions
│   └── travel_planner.py  # Main application
├── tests/                 # Unit tests
├── config/                # Configuration files
├── examples/              # Example usage
└── docs/                  # Documentation
```

## 💰 Cost
Approximately $1-4 in API calls per trip planning session.

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License
MIT License
