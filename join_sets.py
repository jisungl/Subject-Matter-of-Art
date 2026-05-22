import pandas as pd
import os

# path
FOLDER = r"C:\Users\jisun\OneDrive\Documents\school\art209"
OBJECTS_PATH = os.path.join(FOLDER, "objects.csv")
TERMS_PATH = os.path.join(FOLDER, "objects_terms.csv")
OUTPUT_PATH = os.path.join(FOLDER, "nga_set.csv")

objects = pd.read_csv(OBJECTS_PATH, low_memory=False)
terms = pd.read_csv(TERMS_PATH, low_memory=False)

# theme tags
themes = (
    terms[terms.termtype == "Theme"][["objectid", "visualbrowsertheme"]]
    .dropna(subset=["visualbrowsertheme"])
    .rename(columns={"visualbrowsertheme": "theme"})
)

# school tags
schools = (
    terms[terms.termtype == "School"][["objectid", "term"]]
    .drop_duplicates(subset="objectid", keep="first")
    .rename(columns={"term": "school"})
)

obj_cols = [
    "objectid", "title", "classification", "subclassification",
    "medium", "beginyear", "endyear", "displaydate",
    "visualbrowsertimespan", "departmentabbr", "creditline",
    "accessionnum"
]
obj = objects[obj_cols].copy()

merged = obj.merge(schools, on="objectid", how="inner")
merged = merged.merge(themes, on="objectid", how="inner")
merged = merged[merged.beginyear.notna()].copy()

merged.loc[merged.theme == "still", "theme"] = "still life"

# 10 themes
top_themes = [
    "portrait", "genre", "figure", "architecture", "non-representational",
    "landscape", "animal", "religious", "object", "still life"
]
merged = merged[merged.theme.isin(top_themes)]

merged["century"] = (merged.beginyear // 100 * 100).astype(int)
merged["half_century"] = (merged.beginyear // 50 * 50).astype(int)
merged["acq_year"] = merged.accessionnum.str.extract(r"^(\d{4})\.").astype(float)

# 1400-2000
merged = merged[(merged.century >= 1400) & (merged.century <= 2000)]

merged.to_csv(OUTPUT_PATH, index=False)