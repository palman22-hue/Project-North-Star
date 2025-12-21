# Project North Star

## Setup

### Local Development

1. Clone repository
2. Create virtual environment:

python -m venv venv
.\venv\Scripts\Activate # Windows
source venv/bin/activate # Linux/Mac


3. Install dependencies:

pip install -r requirements.txt


4. Create `.env` file with your Mistral API key:

MISTRAL_API_KEY=your_key_here


5. Run:

python api.py

Or use the convenience batch file (Windows):

start_pda.bat


6. Open http://127.0.0.1:8000

### GitHub Codespaces

1. Fork/Clone this repository
2. Open in Codespaces
3. Add your Mistral API key as a **Codespaces Secret**:
- Go to: https://github.com/settings/codespaces
- Click "New secret"
- Name: `MISTRAL_API_KEY`
- Value: your Mistral API key
- Select this repository
4. **Rebuild the container** (Command Palette → "Codespaces: Rebuild Container")
5. Install dependencies:

pip install -r requirements.txt

6. Run:

python api.py

7. Click "Open in Browser" when prompted


