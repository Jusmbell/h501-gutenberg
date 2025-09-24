def list_authors_by_languages(df, alias=True):
    col = "alias" if alias and "alias" in df.columns else "author"
    return (
        df.groupby(col)["language"]
          .nunique()
          .sort_values(ascending=False)
          .index.tolist()
    )

def plot_translations(df, over="birth_century"):
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    if "birth_year" not in df.columns:
        raise ValueError("DataFrame must include 'birth_year'")

    # Clean & derive century
    tmp = df.copy()
    tmp["birth_year"] = pd.to_numeric(tmp["birth_year"], errors="coerce")
    tmp = tmp.dropna(subset=["birth_year"])
    tmp["birth_century"] = (tmp["birth_year"] // 100) * 100

    # --- robust per-author table (1 row per author) ---
    # birth_century: take the first (authors should have one)
    # n_languages: unique languages per author
    per_author = (
        tmp.groupby("author")
           .agg(birth_century=("birth_century", "first"),
                n_languages=("language", "nunique"))
           .reset_index()
           .dropna(subset=["birth_century"])
    )

    # ensure 1-D numeric types (avoids seaborn "Data must be 1-dimensional")
    per_author["birth_century"] = per_author["birth_century"].astype(int)
    per_author["n_languages"]   = pd.to_numeric(per_author["n_languages"], errors="coerce")

    # --- plot ---
    sns.barplot(data=per_author, x="birth_century", y="n_languages", errorbar="ci")
    plt.xlabel("Birth century")
    plt.ylabel("Average number of languages")
    plt.title("Average language count by author birth century")
    plt.tight_layout()
    plt.show()
