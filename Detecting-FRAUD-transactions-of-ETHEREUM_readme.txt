# 🔐 Ethereum Fraud Detection - Flask Web Application

A machine learning-powered web application for detecting fraudulent Ethereum transactions using Flask framework.

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

## 🌟 Features

- **Multi-Model Predictions**: Uses 3 ML models (Logistic Regression, SVM, KNN)
- **Real-time Analysis**: Instant fraud detection for transactions
- **Beautiful UI**: Modern gradient design with animated cards
- **Confidence Scores**: Probability distributions for each model
- **Model Performance**: View detailed metrics and confusion matrices
- **Downloadable Reports**: Access performance CSVs and charts

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | 98.1% | 92.9% | 91.1% | 91.8% | 0.969 |
| SVM | 98.4% | 93.2% | 91.7% | 92.4% | 0.971 |
| KNN | 98.76% | 94.45% | 92.45% | 93.45% | 0.977 |

## 🚀 Live Demo

**Deployed on**: https://detecting-fraud-transactions-of-ethereum.onrender.com/

## 🛠️ Installation & Local Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ethereum-fraud-detection.git
cd ethereum-fraud-detection
```

2. **Create virtual environment (recommended)**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r webapp/requirements.txt
```

4. **Run the Flask app**
```bash
cd webapp
python app.py
```

5. **Open in browser**
Navigate to `http://localhost:5000`

## 📁 Project Structure

```
ethereum-fraud-detection/
├── webapp/
│   ├── app.py                    # Flask application
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Docker configuration
│   ├── templates/
│   │   └── index.html           # Web interface
│   └── sample.csv               # Sample data
├── exports/
│   ├── models/
│   │   ├── LogisticRegression_best.pkl
│   │   ├── SVM_best.pkl
│   │   └── KNN_best.pkl
│   ├── preprocessors/
│   │   ├── scaler.pkl
│   │   ├── feature_names.json
│   │   └── scaler_meta.json
│   └── results/
│       ├── Final_Model_Performance.csv
│       ├── Model_Performance_Summary.csv
│       ├── Feature_Importance.csv
│       └── *_ConfusionMatrix.png
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🎯 How to Use

### Web Interface

1. **Enter Transaction Details**:
   - Transaction Count
   - Balance (ETH)
   - Average Gas Used
   - Token Transfers
   - Total ETH Received
   - Total ETH Sent

2. **Click "Analyze Transaction"**

3. **View Results**:
   - Individual predictions from each model
   - Confidence scores with visual progress bars
   - Color-coded badges (Red = Fraud, Green = Legitimate)

### API Usage (Optional)

```python
import requests

# Prepare transaction data
data = {
    'TxnCount': 150,
    'Balance': 1.5,
    'AvgGasUsed': 21000,
    'TokenTransfers': 10,
    'TotalEthReceived': 5.2,
    'TotalEthSent': 3.8
}

# Make prediction request
response = requests.post('http://localhost:5000/predict', data=data)
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
cd webapp
docker build -t ethereum-fraud-detection .
```

### Run Docker Container

```bash
docker run -p 5000:5000 ethereum-fraud-detection
```

Access at `http://localhost:5000`

## ☁️ Cloud Deployment Options

### Option 1: Render (Free & Easy)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Sign up/Login
4. Click "New" → "Web Service"
5. Connect your GitHub repository
6. Configure:
   - **Name**: ethereum-fraud-detection
   - **Environment**: Python 3
   - **Build Command**: `pip install -r webapp/requirements.txt`
   - **Start Command**: `cd webapp && python app.py`
   - **Port**: 5000
7. Click "Create Web Service"

### Option 2: Heroku

```bash
# Install Heroku CLI, then:
heroku login
heroku create ethereum-fraud-detection
git push heroku main
heroku open
```

**Note**: Create `Procfile` in root:
```
web: cd webapp && gunicorn app:app
```

And add `gunicorn` to `requirements.txt`

### Option 3: PythonAnywhere

1. Upload code via Files
2. Create a web app
3. Configure WSGI file to point to `webapp/app.py`
4. Reload app

### Option 4: Railway

1. Connect GitHub repo
2. Railway auto-detects Flask app
3. Automatic deployment on push

## 📦 Files to Push to GitHub

### ✅ Essential Files (MUST PUSH):

```
✅ webapp/
   ├── app.py                    # Flask app
   ├── requirements.txt          # Dependencies
   ├── Dockerfile               # Docker config
   ├── templates/
   │   └── index.html           # UI
   └── sample.csv               # Sample data
✅ exports/                      # All model files
   ├── models/
   ├── preprocessors/
   └── results/
✅ .gitignore                    # Ignore rules
✅ README.md                     # Documentation
```

### ❌ Files to EXCLUDE:

```
❌ .venv/                        # Virtual environment
❌ __pycache__/                  # Python cache
❌ *.ipynb                       # Jupyter notebooks
❌ .ipynb_checkpoints/           # Notebook checkpoints
❌ transaction_dataset.csv       # Large dataset (optional)
```

## 🔧 Environment Variables (for production)

Create `.env` file (don't commit to GitHub):

```env
FLASK_APP=webapp/app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
PORT=5000
```

## 📊 Features Analyzed

| Feature | Description | Input Type |
|---------|-------------|------------|
| **TxnCount** | Total number of transactions | Integer |
| **Balance** | Current account balance in ETH | Float |
| **AvgGasUsed** | Average gas consumed | Float |
| **TokenTransfers** | ERC20 token transfer count | Integer |
| **TotalEthReceived** | Cumulative ETH received | Float |
| **TotalEthSent** | Cumulative ETH sent | Float |

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Models Not Loading
- Ensure `exports/` folder is present
- Check file paths in `app.py`
- Verify `.pkl` files exist

### Template Not Found
- Verify `templates/index.html` exists
- Check Flask template folder configuration

## 🔒 Security Notes

For production deployment:
- Change `app.secret_key` to a secure random value
- Set `debug=False` in `app.run()`
- Use environment variables for sensitive data
- Add authentication if needed
- Use HTTPS (SSL/TLS)
- Add rate limiting

## 📈 Performance

- **Response Time**: < 100ms per prediction
- **Concurrent Users**: Supports 100+ with proper hosting
- **Model Size**: ~5MB total (all 3 models)

## 🎨 UI Features

- **Modern Design**: Gradient backgrounds, animated cards
- **Responsive**: Works on desktop, tablet, and mobile
- **Color-coded Results**: Visual indicators for fraud/legitimate
- **Progress Bars**: Confidence score visualization
- **Icons**: Font Awesome integration
- **Smooth Animations**: CSS transitions and effects

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with input form |
| `/predict` | POST | Submit transaction for analysis |
| `/results/<filename>` | GET | Download result files |

## 🧪 Testing

Test with sample data:

```bash
curl -X POST http://localhost:5000/predict \
  -d "TxnCount=150" \
  -d "Balance=1.5" \
  -d "AvgGasUsed=21000" \
  -d "TokenTransfers=10" \
  -d "TotalEthReceived=5.2" \
  -d "TotalEthSent=3.8"
```

## 📄 License

This project is for educational purposes.

## 👤 Author

**Abhi Virani**
- GitHub: [@AbhiGuru25](https://github.com/AbhiGuru25)

## 🙏 Acknowledgments

- Dataset: Ethereum Fraud Detection Dataset
- Framework: Flask
- ML Library: Scikit-learn
- UI: Bootstrap 5, Font Awesome

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: abhivirani2556@gmail.com

---

**⭐ If this project helps you, please give it a star!**

