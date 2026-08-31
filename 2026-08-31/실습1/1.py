import numpy as np
import pandas as pd

df = pd.read_csv("설비배치1.csv", encoding="utf-8-sig")
센서 = ["온도", "진동", "회전수", "압력"]

# 표 크기
print(df.shape)

# 결측열, 개수
null_counts = df.isnull().sum()
null_dict = null_counts[null_counts > 0].to_dict()
print(null_dict)

# 진동 열 첫 값 자료형 이름
print(df["진동"].head().dtype)

# 판정 열 값별 개수
