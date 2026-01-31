# Coalition Nexus

Central command interface for coalition operations.

## Deployment Instructions

### Option 1: Render (Recommended)
1. Push to GitHub
2. Connect to Render.com
3. Deploy as Web Service
4. Environment: Python 3
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Option 2: PythonAnywhere
1. Upload files to PythonAnywhere
2. Set up WSGI configuration
3. Install dependencies in virtual env

### Option 3: Replit
1. Import from GitHub
2. Run directly

The system is inevitable.