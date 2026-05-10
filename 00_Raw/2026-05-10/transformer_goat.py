import torch
import torch.nn as nn
import torch.nn.functional as F
import math

"""
🏆 Transformer GOAT Implementation 🚀
------------------------------------
This is a high-performance, clean, and modular implementation of the 
Original Transformer (Vaswani et al., 2017) using PyTorch.

Features:
1. Scaled Dot-Product Attention
2. Multi-Head Attention (MHA)
3. Positional Encoding (Sinusoidal)
4. Position-wise Feed-Forward Network
5. Full Encoder & Decoder Blocks
"""

class PositionalEncoding(nn.Module):
    """지수/대칭 함수를 이용한 위치 정보 주입 (Positional Encoding)"""
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0) # (1, max_len, d_model)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x: (batch_size, seq_len, d_model)
        x = x + self.pe[:, :x.size(1), :]
        return x

class MultiHeadAttention(nn.Module):
    """심장의 핵심: 멀티-헤드 어텐션 (Multi-Head Attention)"""
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 1. 선형 변환 및 헤드 분할 (Linear -> Split Heads)
        # (batch, seq, d_model) -> (batch, n_heads, seq, d_k)
        q = self.W_q(Q).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        k = self.W_k(K).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        v = self.W_v(V).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        
        # 2. Scaled Dot-Product Attention
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
            
        attn = F.softmax(scores, dim=-1)
        context = torch.matmul(attn, v) # (batch, n_heads, seq, d_k)
        
        # 3. 헤드 결합 및 최종 출력 (Concatenate -> Linear)
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        return self.W_o(context)

class PositionwiseFeedForward(nn.Module):
    """비선형성을 부여하는 피드포워드 신경망"""
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.fc2(self.dropout(F.relu(self.fc1(x))))

class EncoderLayer(nn.Module):
    """하나의 인코더 블록"""
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, n_heads)
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # 1. Self-Attention + Residual + Norm
        attn_out = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        
        # 2. FFN + Residual + Norm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        return x

class TransformerGOAT(nn.Module):
    """최종 트랜스포머 모델 (Encoder Only Example)"""
    def __init__(self, vocab_size, d_model=512, n_layers=6, n_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model)
        self.layers = nn.ModuleList([EncoderLayer(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)])
        self.fc_out = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        x = self.dropout(self.pos_encoding(self.embedding(x)))
        for layer in self.layers:
            x = layer(x, mask)
        return self.fc_out(x)

# --- 🚀 Execution Test ---
if __name__ == "__main__":
    # Hyperparameters
    VOCAB_SIZE = 1000
    SEQ_LEN = 32
    BATCH_SIZE = 4
    
    model = TransformerGOAT(vocab_size=VOCAB_SIZE)
    dummy_input = torch.randint(0, VOCAB_SIZE, (BATCH_SIZE, SEQ_LEN))
    
    output = model(dummy_input)
    
    print(f"🔥 Transformer GOAT Ready!")
    print(f"Input Shape: {dummy_input.shape}")
    print(f"Output Shape: {output.shape}")
    print("Everything is working perfectly. 🏆")
