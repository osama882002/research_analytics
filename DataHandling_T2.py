import pandas as pd


# =========================================================
# STEP 1: CLEANING FUNCTIONS
# =========================================================

def clean_researchers(df):

    print("\nCleaning researchers dataset...")
    df['last_name'] = df['last_name'].fillna('')

    df = df.drop_duplicates()

    print("Researchers dataset cleaned!")

    return df

def clean_publications(df):

    print("\nCleaning publications dataset...")

    df = df.drop_duplicates()


    df['title'] = df['title'].fillna(
        'Unknown Title'
    )


    df['citations'] = pd.to_numeric(
        df['citations'],
        errors='coerce'
    )

    df = df[df['citations'] >= 0]

    print("Publications dataset cleaned!")

    return df

def clean_funding(df):

    print("\nCleaning funding dataset...")

    df['amount_cad'] = pd.to_numeric(
        df['amount_cad'],
        errors='coerce'
    )

    df = df[df['amount_cad'] > 0]

    print("Funding dataset cleaned!")

    return df

# =========================================================
# STEP 2: LOAD DATASETS
# =========================================================

print("=== STEP 1: LOADING DATASETS ===")

df_researchers = pd.read_csv('data_row/researchers.csv')
df_publications = pd.read_json('data_row/publications.json')
df_funding = pd.read_excel('data_row/funding.xlsx')

print("Datasets loaded successfully!")

# =========================================================
# STEP 3: INITIAL EXPLORATION (EDA)
# =========================================================

print("\n=== STEP 2: EXPLORING DATASETS ===")

# ==============Researchers Dataset=====================

print("\n== Researchers Dataset ==")

print("\nFirst 5 Rows:")
print(df_researchers.head())

print("\nDataset Shape:")
print(df_researchers.shape)

print("\nColumns:")
print(df_researchers.columns)

print("\nDataset Info:")
print(df_researchers.info())

print("\nMissing Values:")
print(df_researchers.isnull().sum())

print("\nDuplicate Rows:")
print(df_researchers.duplicated().sum())

# ===============Publications Dataset===================== 

print("\n== Publications Dataset ==")

print("\nFirst 5 Rows:")
print(df_publications.head())

print("\nDataset Shape:")
print(df_publications.shape)

print("\nColumns:")
print(df_publications.columns)

print("\nDataset Info:")
print(df_publications.info())

print("\nMissing Values:")
print(df_publications.isnull().sum())

print("\nDuplicate Rows:")
print(df_publications.duplicated().sum())

# ===============Funding Dataset=====================

print("\n== Funding Dataset ==")

print("\nFirst 5 Rows:")
print(df_funding.head())

print("\nDataset Shape:")
print(df_funding.shape)

print("\nColumns:")
print(df_funding.columns)

print("\nDataset Info:")
print(df_funding.info())

print("\nMissing Values:")
print(df_funding.isnull().sum())

print("\nDuplicate Rows:")
print(df_funding.duplicated().sum())


# =========================================================
# STEP 4: CLEAN DATA
# =========================================================

print("\n=== STEP 3: CLEANING DATA ===")

df_researchers = clean_researchers(df_researchers)
df_publications = clean_publications(df_publications)
df_funding = clean_funding(df_funding)

# =========================================================
# STEP 5: CP1 RESEARCHERS ANALYSIS
# =========================================================

print("\n=== STEP 5: CP1 RESEARCHERS ANALYSIS ===")

# Sort researchers by joined year 
sorted_researchers = (
    df_researchers
    .sort_values(
    by='joined_year'
    ,ascending=True
    )
    )

# filter active researchers with h_index > 15
filtered_researchers = (
    sorted_researchers
    .query('is_active and h_index > 15')
    )

# Extract first letter from last names
secret_word = (
    filtered_researchers['last_name']
    .str[0]
    .str.upper()
    .str.cat()
)

print("Secret Word:", secret_word)

# =========================================================
# STEP 6: CP2 PUBLICATIONS ANALYSIS
# =========================================================

print("\n=== STEP 6: CP2 PUBLICATIONS ANALYSIS ===")

# paper with highest citations
top_paper = df_publications.loc[
    df_publications['citations'].idxmax()
]

# Extract title of the top paper
top_title = top_paper['title']

print("Most Cited Paper:" , top_title)

# Compare title with secret word
clean_secret = (
    secret_word
    .replace(" ", "")
    .replace(":", "")
    .lower()
)

clean_title = (
    top_title
    .replace(" ", "")
    .replace(":", "")
    .lower()
)

if clean_secret in clean_title:
    print("Secret word is in the title!")
else:
    print("Secret word is NOT in the title.")

# =========================================================
# STEP 7: CP3 FUNDING ANALYSIS
# =========================================================    

print("\n=== STEP 7: CP3 FUNDING ANALYSIS ===")

# Sum funding amounts
total_funding = (
    df_funding['amount_cad']
    .sum()
)

# Extract encoded year
year = int(
    str(int(total_funding))[:4]
)

print(f"Total Funding: ${int(total_funding):,}")
print(f"Encoded Year: {year}")


# =========================================================
# STEP 8: VALIDATE RELATIONSHIPS
# =========================================================

print("\n=== STEP 8: VALIDATING RELATIONSHIPS ===")

# Check publication researcher IDs
publication_check = (
    df_publications['researcher_id']
    .isin(df_researchers['researcher_id'])
    .all()
)
print("All publication researcher IDs exist:", publication_check)

# Check funding researcher IDs
funding_check = (
    df_funding['researcher_id']
    .isin(df_researchers['researcher_id'])
    .all()
)
print("All funding researcher IDs exist:", funding_check)