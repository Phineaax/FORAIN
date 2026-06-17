"""
Construit un DataFrame pandas avec les colonnes :
    - file_name
    - catégorie
    - description
    - transcription

Les descriptions sont lues dans :
    ./descriptions/GPT Mini prompt 1/{catégorie}/{file_name}.txt
Les transcriptions sont lues dans :
    ./transcriptions/{catégorie}/{file_name}.txt

Le résultat est enregistré dans : table_transcriptions_descriptions.csv
"""

from pathlib import Path
import pandas as pd

DESCRIPTIONS_DIR = Path("./descriptions/GPT Mini prompt 1")
TRANSCRIPTIONS_DIR = Path("./transcriptions")
OUTPUT_CSV = "table_transcriptions_descriptions.csv"


def read_text(path: Path) -> str | None:
    """Lit le contenu d'un fichier texte, ou retourne None s'il n'existe pas."""
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return None


def build_dataframe() -> pd.DataFrame:
    rows = []

    # On parcourt tous les fichiers .txt de descriptions, organisés par catégorie
    for description_path in sorted(DESCRIPTIONS_DIR.glob("*/*.txt")):
        categorie = description_path.parent.name
        file_name = description_path.stem  # nom sans l'extension .txt

        description = read_text(description_path)

        transcription_path = TRANSCRIPTIONS_DIR / categorie / f"{file_name}.txt"
        transcription = read_text(transcription_path)

        if transcription is None:
            print(f"⚠️  Transcription manquante pour : {categorie}/{file_name}")

        rows.append(
            {
                "file_name": file_name,
                "catégorie": categorie,
                "description": description,
                "transcription": transcription,
            }
        )

    return pd.DataFrame(rows, columns=["file_name", "catégorie", "description", "transcription"])


if __name__ == "__main__":
    df = build_dataframe()
    print(f"{len(df)} lignes construites.")
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Fichier enregistré : {OUTPUT_CSV}")