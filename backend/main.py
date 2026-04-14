from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import torch
import os
from typing import List

# Import our custom modules
import database, models, schemas, auth

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="RAPOS Deep Learning API", version="1.1.0")

# --- CORS SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY SETUP ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        from jose import jwt
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- MODEL LOADING ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'lstm_model.pth')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'data', 'scaler_params.npy')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'simulated_stocks.csv')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class StockLSTM(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(StockLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = torch.nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = torch.nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

loaded_model = None
scaler_scale = None
scaler_min = None
SEQUENCE_LENGTH = 60

@app.on_event("startup")
def load_assets():
    global loaded_model, scaler_scale, scaler_min, SEQUENCE_LENGTH
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            print("Loading LSTM model and scaler...")
            checkpoint = torch.load(MODEL_PATH, map_location=device)
            loaded_model = StockLSTM(
                input_size=checkpoint['input_size'],
                hidden_size=checkpoint['hidden_size'],
                num_layers=checkpoint['num_layers'],
                output_size=checkpoint['output_size']
            ).to(device)
            loaded_model.load_state_dict(checkpoint['model_state_dict'])
            loaded_model.eval()
            SEQUENCE_LENGTH = checkpoint['sequence_length']
            scaler_params = np.load(SCALER_PATH)
            scaler_scale = scaler_params[0]
            scaler_min = scaler_params[1]
            print("Model loaded successfully.")
        else:
            print("WARNING: Model files not found. Ensure train_lstm.py has been run.")
    except Exception as e:
        print(f"Error loading model: {e}")

# --- AUTH ENDPOINTS ---

@app.post("/api/auth/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_name": user.full_name
    }

# --- APPLICATION ENDPOINTS ---

@app.get("/api/user/profile", response_model=schemas.User)
def get_user_profile(user: models.User = Depends(get_current_user)):
    return user

@app.get("/api/predict-risk")
def predict_risk(ticker: str = 'SPXX'):
    global loaded_model, scaler_scale, scaler_min
    
    if loaded_model is None:
        # Fallback for demo stability if model hasn't been trained yet
        return {
            "ticker": ticker,
            "ai_risk_score": 5.0,
            "message": "Demo Mode: Model not trained, showing average risk baseline."
        }
        
    try:
        df = pd.read_csv(DATA_PATH)
        df_ticker = df[df['Ticker'] == ticker].copy()
        if len(df_ticker) < SEQUENCE_LENGTH:
            raise HTTPException(status_code=400, detail=f"Not enough data for {ticker}.")
            
        recent_data = df_ticker['Close'].values[-SEQUENCE_LENGTH:]
        scaled_inputs = recent_data * scaler_scale + scaler_min
        input_tensor = torch.tensor(scaled_inputs, dtype=torch.float32).view(1, SEQUENCE_LENGTH, 1).to(device)
        
        with torch.no_grad():
            scaled_prediction = loaded_model(input_tensor).item()
            
        predicted_price = (scaled_prediction - scaler_min) / scaler_scale
        recent_returns = pd.Series(recent_data).pct_change().dropna()
        annual_volatility = recent_returns.std() * np.sqrt(252) * 100
        last_close = recent_data[-1]
        predicted_return = ((predicted_price - last_close) / last_close) * 100
        risk_score = min(max((annual_volatility / 3.0), 1.0), 10.0)
        
        return {
            "ticker": ticker,
            "last_close_price": round(float(last_close), 2),
            "predicted_next_close": round(float(predicted_price), 2),
            "predicted_daily_return_pct": round(float(predicted_return), 2),
            "historical_volatility_pct": round(float(annual_volatility), 2),
            "ai_risk_score": round(float(risk_score), 1),
            "model_type": "LSTM Neural Network"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
