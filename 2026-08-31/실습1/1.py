import numpy as np
import pandas as pd

df = pd.read_csv("설비배치1.csv", encoding="utf-8-sig")
센서 = ["온도", "진동", "회전수", "압력"]

# 1
# 표 크기
print(df.shape)

# 결측열, 개수
null_counts = df.isnull().sum()
null_dict = null_counts[null_counts > 0].to_dict()
print(null_dict)

# 진동 열 첫 값 자료형 이름
print(df["진동"].head().dtype)

# 판정 열 값별 개수
alarm_dict = df["판정"].value_counts().to_dict()
print(alarm_dict)

# 2
df["진동"] = pd.to_numeric(df["진동"], errors="coerce")

결측개수 = df["진동"].isna().sum()
평균값 = round(df["진동"].mean(), 2)

print(결측개수)
print(평균값)

# 3
print(df.duplicated().sum())
df = df.drop_duplicates()
print(df.shape)

# 4
# 온도는 온도 열 전체 평균으로, 압력은 압력 열 전체 중앙값으로,
# 진동은 진동 열 전체 평균으로 채우세요.

df["온도"] = df["온도"].fillna(df["온도"].mean().round(2))
df["압력"] = df["압력"].fillna(df["압력"].median().round(2))
df["진동"] = df["진동"].fillna(df["진동"].mean().round(2))


sensor_null_counts = df[["온도", "압력", "진동", "회전수"]].isna().sum().sum()
print(sensor_null_counts)
print(np.round(df["온도"].mean(), 2), np.round(df["압력"].median(), 2))


# 5
line = df.groupby("생산라인")[["온도", "진동", "회전수", "압력"]].mean().round(2)
print(line)

line_dict = df["생산라인"].value_counts().sort_index().to_dict()
print(line_dict)

# 6
# 온도 열 전체의 평균과 표준편차(ddof=0)를 소수 둘째 자리로 한 줄에 출력하세요.
print(df["온도"].mean().round(2), df["온도"].std(ddof=0).round(2))
z = (df["온도"] - df["온도"].mean()) / df["온도"].std()
print((z.abs() > 3).sum(), (z.abs() > 2).sum())

# 7
q1, q3 = np.percentile(df["압력"], 25), np.percentile(df["압력"], 75)
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(low.round(2), high.round(2))
mask = (df["압력"] < low) | (df["압력"] > high)
print(len(df["압력"][mask]))

pre_err = df.loc[mask, "생산라인"].value_counts().to_dict()
print(pre_err)


# 8

df = df[~mask].reset_index(drop=True)

line_dict = df["생산라인"].value_counts().sort_index().to_dict()

print(df["생산라인"].value_counts().sort_index().to_dict())
print(df["생산라인"].value_counts().sort_index().to_dict())
print(df.shape)

# 9
cols = ["온도", "진동", "회전수", "압력"]

cols_minmax = {c: {"min": float(df[c].min()), "max": float(df[c].max())} for c in cols}
print(cols_minmax)

df_copy = df.copy()
for c in cols:
    lo = cols_minmax[c]["min"]
    hi = cols_minmax[c]["max"]
    df_copy[c] = ((df_copy[c] - lo) / (hi - lo)).round(3)
print(df_copy[cols])

min_values = df_copy[cols].min().round(3).to_dict()
max_values = df_copy[cols].max().round(3).to_dict()
mean_values = df_copy[cols].mean().round(3).to_dict()
print(min_values)
print(max_values)
print(mean_values)

# 정규화 열 추가
new_df = df_copy[["검사일시", "생산라인"] + cols].round(4)
new_df.to_csv("정규화_멘티.csv", index=False, encoding="utf-8-sig")
print(new_df.shape)

# 10
df["라인코드"] = df["생산라인"].map({"A라인": 0, "B라인": 1, "C라인": 2})
final = df[
    ["검사일시", "생산라인", "라인코드", "온도", "진동", "회전수", "압력", "판정"]
]
final.to_csv("정제결과_멘티.csv", index=False, encoding="utf-8-sig")

# 다시 읽기
f = pd.read_csv("정제결과_멘티.csv", encoding="utf-8-sig")

# 결측열, 개수
f_null_counts = f.isnull().sum().sum()
f_duplicated_counts = f.duplicated().sum()
print(f.shape, f_null_counts, f_duplicated_counts)
print(f.columns.tolist())
