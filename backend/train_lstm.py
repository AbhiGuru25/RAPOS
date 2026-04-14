import pandas as pd
import numpy as np
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

# --- 1. CONFIGURATION ---
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'simulated_stocks.csv')
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), 'lstm_model.pth')
TICKER_TO_PREDICT = 'SPXX'
SEQUENCE_LENGTH = 60 # Use past 60 days to predict the next day
EPOCHS = 20
BATCH_SIZE = 32
LEARNING_RATE = 0.001

# --- 2. DATA PREPARATION ---
class StockDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

def load_and_preprocess_data():
    print(f"Loading data from {DATA_FILE}")
    df = pd.read_csv(DATA_FILE)
    
    # Filter for the specific ticker
    df = df[df['Ticker'] == TICKER_TO_PREDICT].copy()
    
    # We will use 'Close' price for prediction, but can supply multiple features (e.g. Volume)
    features = ['Close'] 
    
    # Scale the data (LSTMs are sensitive to scale)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[features])
    
    X, y = [], []
    for i in range(SEQUENCE_LENGTH, len(scaled_data)):
        X.append(scaled_data[i-SEQUENCE_LENGTH:i]) 
        y.append(scaled_data[i, 0]) # Target is the close price at the current step
        
    X, y = np.array(X), np.array(y)
    
    # Split into train and test sets (80% train, 20% test)
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    return X_train, y_train, X_test, y_test, scaler

# --- 3. MODEL DEFINITION ---
class StockLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(StockLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM Layer
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        
        # Fully connected output layer
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # Initialize hidden state and cell state
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

# --- 4. TRAINING ROUTINE ---
def train_model():
    # Detect device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load data
    X_train, y_train, X_test, y_test, scaler = load_and_preprocess_data()
    
    train_dataset = StockDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    # Initialize model
    input_size = 1 # We are only using 'Close' price as feature
    hidden_size = 50
    num_layers = 2
    output_size = 1 # Predicting a single value (next day's close)
    
    model = StockLSTM(input_size, hidden_size, num_layers, output_size).to(device)
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    print("Starting training...")
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        
        for batch_i, (inputs, targets) in enumerate(train_loader):
            inputs, targets = inputs.to(device), targets.to(device)
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs.squeeze(), targets)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        avg_loss = total_loss / len(train_loader)
        
        # Validation
        model.eval()
        with torch.no_grad():
            test_inputs = torch.tensor(X_test, dtype=torch.float32).to(device)
            test_targets = torch.tensor(y_test, dtype=torch.float32).to(device)
            test_outputs = model(test_inputs)
            test_loss = criterion(test_outputs.squeeze(), test_targets).item()
            
        print(f"Epoch [{epoch+1}/{EPOCHS}], Train Loss: {avg_loss:.6f}, Val Loss: {test_loss:.6f}")
        
    print("Training finished!")
    
    # Save the model
    torch.save({
        'model_state_dict': model.state_dict(),
        'input_size': input_size,
        'hidden_size': hidden_size,
        'num_layers': num_layers,
        'output_size': output_size,
        'sequence_length': SEQUENCE_LENGTH
    }, MODEL_SAVE_PATH)
    
    # Save the scaler bounds so the API can use them
    scaler_params_path = os.path.join(os.path.dirname(__file__), 'data', 'scaler_params.npy')
    np.save(scaler_params_path, np.array([scaler.scale_[0], scaler.min_[0]]))
    
    print(f"Model saved to: {MODEL_SAVE_PATH}")
    print(f"Scaler parameters saved to: {scaler_params_path}")

if __name__ == "__main__":
    train_model()
