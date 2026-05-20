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
