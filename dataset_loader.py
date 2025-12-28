import os
import shutil

def load_kaggle_resumes(domain_folder, limit=5):
    SOURCE_DIR = f"data/kaggle_resumes/{domain_folder}"
    TARGET_DIR = "data/resumes"

    if not os.path.exists(SOURCE_DIR):
        raise ValueError(f"❌ Domain folder not found: {SOURCE_DIR}")

    os.makedirs(TARGET_DIR, exist_ok=True)

    # Clear existing resumes
    for file in os.listdir(TARGET_DIR):
        os.remove(os.path.join(TARGET_DIR, file))

    # Copy resumes
    for file in os.listdir(SOURCE_DIR)[:limit]:
        shutil.copy(
            os.path.join(SOURCE_DIR, file),
            os.path.join(TARGET_DIR, file)
        )

    print(f"✅ Loaded {limit} resumes from '{domain_folder}' domain.")
