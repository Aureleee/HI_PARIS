"""t6 / M3 — Transformer regressor with 2 heads (Mendes & Martins 2023), trained FROM SCRATCH,
and the "small vs bigger" question of Kim et al. 2024 (compare model sizes).
Mendes fine-tune pretrained multilingual transformers (forbidden here): we keep the setup
(encoder -> mean pooling -> valence/arousal heads with sigmoid) but learn everything from zero.
Tokens: lowercase words hashed into a fixed vocab (no pretrained tokenizer).
Usage: python tracks/t6_papers/m3_small_transformer.py [tiny|small] [n_rows] [epochs]"""
import re
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np
import torch
import torch.nn as nn

from src.common import TARGETS, folds, load, log_result, write_submission

size = sys.argv[1] if len(sys.argv) > 1 else "tiny"
n_rows = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "all" else None
epochs = int(sys.argv[3]) if len(sys.argv) > 3 else 2
D, L = {"tiny": (64, 1), "small": (192, 3)}[size]
V, T = 2**17, 256  # hashed vocab, max tokens
torch.manual_seed(2026)

tr = load("x_train_final", ["id", "clean_text"]).merge(load("y_train"), on="id")
te = load("x_test_final", ["id", "clean_text"])
if n_rows:
    tr = tr.sample(n_rows, random_state=0)
y = tr[TARGETS].to_numpy("float32")
lo, hi = y.min(0), y.max(0)  # targets rescaled to [0,1] for the sigmoid heads


def encode(texts):
    out = np.zeros((len(texts), T), dtype=np.int64)
    for i, s in enumerate(texts):
        ids = [zlib.crc32(w.encode()) % (V - 1) + 1 for w in re.findall(r"\w+", str(s).lower())[:T]]
        out[i, :len(ids)] = ids
    return torch.from_numpy(out)


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.emb, self.pos = nn.Embedding(V, D, padding_idx=0), nn.Embedding(T, D)
        layer = nn.TransformerEncoderLayer(D, 4, 4 * D, 0.1, batch_first=True)
        self.enc, self.head = nn.TransformerEncoder(layer, L), nn.Linear(D, 2)

    def forward(self, x):
        mask = x == 0
        h = self.enc(self.emb(x) + self.pos.weight[: x.shape[1]], src_key_padding_mask=mask)
        h = (h * ~mask[..., None]).sum(1) / (~mask).sum(1, keepdim=True).clamp(min=1)  # mean pooling
        return torch.sigmoid(self.head(h))


def predict(net, X):
    net.eval()
    with torch.no_grad():
        return torch.cat([net(X[i:i + 512]) for i in range(0, len(X), 512)]).numpy() * (hi - lo) + lo


Xtr, Xte = encode(tr["clean_text"].tolist()), encode(te["clean_text"].tolist())
yt = torch.from_numpy((y - lo) / (hi - lo))
fold = folds(tr["id"])
oof, test = np.zeros_like(y), np.zeros((len(te), 2), dtype="float32")
for k in range(5):
    t = torch.from_numpy(np.where(fold != k)[0])
    net = Net()
    opt = torch.optim.AdamW(net.parameters(), 1e-3, weight_decay=0.01)
    for ep in range(epochs):
        net.train()
        for b in t[torch.randperm(len(t))].split(128):
            loss = nn.functional.mse_loss(net(Xtr[b]), yt[b])
            opt.zero_grad(); loss.backward(); opt.step()
        print(f"fold {k} epoch {ep} loss {loss.item():.4f}", flush=True)
    oof[fold == k] = predict(net, Xtr[fold == k])
    test += predict(net, Xte) / 5
name = f"m3_transformer_{size}_e{epochs}" + (f"_n{n_rows}" if n_rows else "")
log_result("t6_papers", name, tr["id"].to_numpy(), y, oof, te["id"].to_numpy(), test,
           notes=f"from scratch, d={D}, layers={L}, hashed vocab {V}")
if not n_rows:
    write_submission(te["id"].to_numpy(), test, f"t6_{name}")
