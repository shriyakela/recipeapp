```bash
# 📦 Step-by-Step Setup for Recipe Book Project

# 1. Clone the repository
git clone https://github.com/your-username/your-recipe-project.git
cd your-recipe-project

# 2. Set up and activate virtual environment (Flask backend)
python -m venv venv

# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the Flask backend
python app.py
# (App runs at http://127.0.0.1:5000)

# 5. Run the Angular frontend
cd frontend

# Install Node dependencies
npm install

# Start Angular development server
ng serve
# (Frontend runs at http://localhost:4200)

# ✅ All Set: Flask running on port 5000, Angular on 4200
```
