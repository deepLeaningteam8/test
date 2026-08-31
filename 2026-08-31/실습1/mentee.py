import numpy as np
import pandas as pd

df = pd.read_csv("설비배치1.csv", encoding="utf-8-sig")
센서 = ["온도", "진동", "회전수", "압력"]

print(df.shape)
