import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_stock_data(tickers, start_date, num_days=1258):
    """
    Generates synthetic daily stock data (Open, High, Low, Close, Volume)
    using a Geometric Brownian Motion (GBM) model.
    1258 trading days is approximately 5 years.
    """
    # Create the business day date range
    dates = pd.date_range(start=start_date, periods=num_days, freq='B')
    
    all_data = []

    for ticker in tickers:
        print(f"Generating data for {ticker}...")
        
        # Initial parameters for the simulation
        # Based on average S&P 500 drift (annual return ~8%) and volatility (~15%)
        mu = 0.08 / 252       # Daily drift
        sigma = 0.15 / np.sqrt(252) # Daily volatility
        
        # Start the stock off at a random price between $50 and $200
        S0 = np.random.uniform(50.0, 200.0)
        
        # Generate random shocks
        dt = 1
        shocks = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt), size=num_days)
        
        # Calculate daily closing prices using cumulative product (Geometric Brownian Motion)
        price_multipliers = np.exp(shocks)
        closes = S0 * np.cumprod(price_multipliers)
        
        # Generate OHLC data from the close price
        # Daily variance to create high/low spreads
        daily_volatility = closes * np.random.uniform(0.005, 0.02, size=num_days)
        
        # Shift close data to use previous day's close as today's open
        opens = np.roll(closes, 1)
        opens[0] = S0  # First day open
        
        # Ensure High is max, Low is min
        highs = np.maximum(opens, closes) + (daily_volatility * np.random.uniform(0.1, 1.0, size=num_days))
        lows = np.minimum(opens, closes) - (daily_volatility * np.random.uniform(0.1, 1.0, size=num_days))
        
        # Generate random trading volume
        base_volume = np.random.randint(1_000_000, 5_000_000)
        volumes = np.random.normal(loc=base_volume, scale=base_volume * 0.2, size=num_days).astype(int)
        volumes = np.clip(volumes, 100_000, 50_000_000) # Floor/Ceiling
        
        # Create a DataFrame for this ticker
        ticker_df = pd.DataFrame({
            'Date': dates,
            'Ticker': ticker,
            'Open': np.round(opens, 2),
            'High': np.round(highs, 2),
            'Low': np.round(lows, 2),
            'Close': np.round(closes, 2),
            'Volume': volumes
        })
        
        # Add technical indicators as features
        ticker_df['Returns'] = ticker_df['Close'].pct_change()
        ticker_df['MA10'] = ticker_df['Close'].rolling(window=10).mean()
        ticker_df['MA50'] = ticker_df['Close'].rolling(window=50).mean()
        ticker_df['Volatility_20d'] = ticker_df['Returns'].rolling(window=20).std() * np.sqrt(252) # Annualized
        
        # Drop the first 50 rows due to NaN values from the MA50
        ticker_df = ticker_df.dropna()
        
        all_data.append(ticker_df)

    # Combine all ticker data
    final_df = pd.concat(all_data, ignore_index=True)
    
    return final_df

if __name__ == "__main__":
    # We will generate data for a simulated S&P 500 Tracker (SPXX), a tech stock (TECH), and a bond fund (BNDX)
    tickers_to_generate = ['SPXX', 'TECH', 'BNDX']
    
    # Start 5 years ago
    start_date = datetime.now() - timedelta(days=5 * 365)
    
    print("Starting simulation...")
    df = generate_stock_data(tickers_to_generate, start_date)
    
    # Save the generated dataset
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, 'simulated_stocks.csv')
    df.to_csv(output_path, index=False)
    
    print(f"✅ Successfully generated {len(df)} rows of data.")
    print(f"Data saved to: {output_path}")
    print("\nSample Preview:")
    print(df.head())
