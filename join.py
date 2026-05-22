import pandas as pd

objects = pd.read_csv(r'C:\Users\jisun\OneDrive\Documents\school\art209\objects.csv', low_memory=False)
terms = pd.read_csv(r'C:\Users\jisun\OneDrive\Documents\school\art209\objects_terms.csv', low_memory=False)

# theme tags
themes = (
    terms[terms.termtype == 'Theme'][['objectid', 'visualbrowsertheme']]
    .dropna(subset=['visualbrowsertheme'])
    .rename(columns={'visualbrowsertheme': 'theme'})
)

# school tags
schools = (
    terms[terms.termtype == 'School'][['objectid', 'term']]
    .drop_duplicates(subset='objectid', keep='first')
    .rename(columns={'term': 'school'})
)
# columns
obj_cols = [
    'objectid', 'title', 'classification', 'subclassification',
    'medium', 'beginyear', 'endyear', 'displaydate',
    'visualbrowsertimespan', 'departmentabbr', 'creditline',
    'accessionnum'
]
obj = objects[obj_cols].copy()
merged = obj.merge(schools, on='objectid', how='inner')
merged = merged.merge(themes, on='objectid', how='inner')
merged = merged[merged.beginyear.notna()].copy()
merged['century'] = (merged.beginyear // 100 * 100).astype(int)
merged['half_century'] = (merged.beginyear // 50 * 50).astype(int)
merged['acq_year'] = merged.accessionnum.str.extract(r'^(\d{4})\.').astype(float)

# save
out_path = r'C:\Users\jisun\OneDrive\Documents\school\art209\nga_set.csv'
merged.to_csv(out_path, index=False)