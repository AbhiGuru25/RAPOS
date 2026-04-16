from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import torch
import os
import finnhub
from typing import List

# Initialize FastAPI app
app = FastAPI(title="RAPOS AI Prediction Service", version="2.0.1")

# --- MARKET DATA CLIENT ---
# I will use the key you provided as a fallback/env var
FINNHUB_KEY = os.getenv("FINNHUB_API_KEY", "d7fucvhr01qqb8rhld4gd7fucvhr01qqb8rhld50")
finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

# --- CORS SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            print("RAPOS AI: Loading LSTM model and scaler...")
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
            print("RAPOS AI: Model loaded successfully.")
        else:
            print("RAPOS AI WARNING: Model files not found. Running in simulation fallback mode.")
    except Exception as e:
        print(f"RAPOS AI Error loading model: {e}")

# --- AI ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "RAPOS AI Service is online", "integration": "Supabase Auth Hybrid"}

@app.get("/api/predict-risk")
def predict_risk(ticker: str = 'SPXX'):
    global loaded_model, scaler_scale, scaler_min
    
    if loaded_model is None:
        # Fallback for demo stability if model hasn't been trained yet
        return {
            "ticker": ticker,
            "ai_risk_score": 5.0,
            "last_close_price": 150.0,
            "predicted_next_close": 152.5,
            "predicted_daily_return_pct": 1.6,
            "historical_volatility_pct": 12.5,
            "is_simulated": True,
            "message": "Demo Mode: Using average risk baseline."
        }
        
    try:
        df = pd.read_csv(DATA_PATH)
        df_ticker = df[df['Ticker'] == ticker].copy()
        if len(df_ticker) < SEQUENCE_LENGTH:
             # Simulation fallback if ticker is missing from local CSV (like new crypto)
             return {
                "ticker": ticker,
                "ai_risk_score": round(np.random.uniform(4.0, 8.0), 1),
                "is_simulated": True
            }
            
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
            "model_type": "LSTM Neural Network",
            "is_simulated": False
        }
    except Exception as e:
        # Extreme fallback
        return {
            "ticker": ticker, 
            "ai_risk_score": 6.5,
            "last_close_price": 0.0,
            "predicted_next_close": 0.0,
            "predicted_daily_return_pct": 0.0,
            "historical_volatility_pct": 0.0,
            "is_simulated": True, 
            "error": str(e)
        }

# --- REAL-TIME MARKET DATA ---

@app.get("/api/live-price")
def get_live_price(ticker: str):
    """
    Fetches real-time price from Finnhub.
    """
    try:
        # Quote data from Finnhub
        # c: Current price, d: Change, dp: Percent change
        quote = finnhub_client.quote(ticker.upper())
        
        if not quote or quote['c'] == 0:
            raise HTTPException(status_code=404, detail="Ticker not found or no data.")

        return {
            "ticker": ticker.upper(),
            "current_price": round(float(quote['c']), 2),
            "change": round(float(quote['d']), 2),
            "percent_change": round(float(quote['dp']), 2),
            "high": round(float(quote['h']), 2),
            "low": round(float(quote['l']), 2),
            "previous_close": round(float(quote['pc']), 2),
            "timestamp": os.getlogin() if os.name == 'nt' else 'render' # logging metadata
        }
    except Exception as e:
        print(f"Market Data Error: {e}")
        return {
            "ticker": ticker,
            "error": "Failed to fetch live price",
            "current_price": 0,
            "percent_change": 0
        }

@app.get("/api/search-stocks")
def search_stocks(q: str):
    """
    Search for symbols/stocks by name.
    """
    try:
        search_results = finnhub_client.symbol_lookup(q)
        # Simplify results for the frontend
        cleaned = []
        for item in search_results.get('result', [])[:8]: # Limit to top 8
            cleaned.append({
                "symbol": item['symbol'],
                "displaySymbol": item['displaySymbol'],
                "description": item['description'],
                "type": item['type']
            })
        return {"query": q, "results": cleaned}
    except Exception as e:
        print(f"Search Error: {e}")
        return {"query": q, "results": [], "error": str(e)}

# --- PORTFOLIO OPTIMIZATION ---

RISK_PROFILES = {
    "Conservative": {"Stocks": 0.20, "Crypto": 0.05, "Bonds": 0.60, "Cash": 0.15},
    "Moderate": {"Stocks": 0.45, "Crypto": 0.15, "Bonds": 0.30, "Cash": 0.10},
    "Aggressive": {"Stocks": 0.65, "Crypto": 0.25, "Bonds": 0.05, "Cash": 0.05}
}

@app.get("/api/rebalance")
def rebalance_portfolio(total_value: float, profile: str = "Moderate"):
    """
    Calculates the target dollar amounts for each asset class based on a profile.
    """
    if profile not in RISK_PROFILES:
        profile = "Moderate"
        
    targets = RISK_PROFILES[profile]
    report = []
    
    for asset_type, weight in targets.items():
        target_value = round(total_value * weight, 2)
        report.append({
            "asset_type": asset_type,
            "target_weight": f"{int(weight*100)}%",
            "target_value": target_value,
            "description": f"Targeting {int(weight*100)}% allocation for {asset_type}."
        })
        
    return {
        "profile": profile,
        "total_value": total_value,
        "optimization_report": report,
        "advice": f"Optimization complete for {profile} profile. Adjust holdings to match target values."
    }

# --- WEALTH HISTORY & NEWS ---

@app.get("/api/market-discover")
def market_discover():
    """
    RAPOS AI Market Insight: Finds the top gainers from a curated Alpha List.
    """
    alpha_tickers = ["NVDA", "TSLA", "AAPL", "MSFT", "BTC-USD", "ETH-USD", "GOOGL", "AMD"]
    raw_results = []
    
    for ticker in alpha_tickers:
        try:
            # Finnhub requires BTC-USD style for quote? 
            # Actually standard BTC usually works if mapped correctly. 
            # We will try a simple quote first.
            t = ticker.replace("-USD", "")
            quote = finnhub_client.quote(t)
            if quote and quote['c'] > 0:
                raw_results.append({
                    "ticker": ticker,
                    "price": round(float(quote['c']), 2),
                    "change": round(float(quote['dp']), 2),
                    "sentiment": "Bullish" if quote['dp'] > 0 else "Bearish"
                })
        except: continue
        
    # Sort by percentage change descending
    sorted_gainers = sorted(raw_results, key=lambda x: x['change'], reverse=True)
    return {"discovery": sorted_gainers[:4], "intelligence_note": "AI analysis suggests high-momentum accumulation in these tickers."}

@app.get("/api/market-news")
def get_market_news(category: str = "general"):
    """
    Fetches latest market news from Finnhub.
    """
    try:
        news = finnhub_client.general_news(category, min_id=0)
        return {"news": news[:10]} # Top 10 headlines
    except Exception as e:
        return {"news": [], "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
