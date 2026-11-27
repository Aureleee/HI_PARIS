# CSV (data/raw) -> parquet float32 (data/processed)
import pathlib
import pandas as pd

RAW, OUT = pathlib.Path("data/raw"), pathlib.Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

for f in sorted(RAW.rglob("*.csv")):
    df = pd.read_csv(f, engine="pyarrow")
    fl = df.select_dtypes("float64").columns
    df[fl] = df[fl].astype("float32")
    df.to_parquet(OUT / f"{f.stem}.parquet", index=False)
    print(f.name, df.shape)
