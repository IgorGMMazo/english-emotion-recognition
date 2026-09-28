"""Download the original English GoEmotions benchmark, preserving its splits."""

import json
from pathlib import Path

from datasets import load_dataset, load_from_disk


DATASET_ID = "google-research-datasets/go_emotions"
CONFIG = "simplified"
REVISION = "add492243ff905527e67aeb8b80c082af02207c3"
DATASET_PATH = Path(__file__).resolve().parent / "datasets" / "go_emotions"
EXPECTED_ROWS = {"train": 43410, "validation": 5426, "test": 5427}


def validate_dataset(dataset):
    """Check split sizes and the original multilabel schema before use."""
    if set(dataset) != set(EXPECTED_ROWS):
        raise ValueError("Unexpected dataset splits")
    names = dataset["train"].features["labels"].feature.names
    if len(names) != 28 or names[-1] != "neutral":
        raise ValueError("Expected 27 emotions followed by neutral")
    for split, rows in EXPECTED_ROWS.items():
        data = dataset[split]
        if len(data) != rows or set(data.column_names) != {"text", "labels", "id"}:
            raise ValueError(f"Unexpected size or columns in {split}")
        if data.features["labels"].feature.names != names:
            raise ValueError(f"Inconsistent label order in {split}")
        for row in data:
            if not row["text"] or not row["id"] or not row["labels"]:
                raise ValueError(f"Missing text, ID or labels in {split}")
            if any(label < 0 or label >= len(names) for label in row["labels"]):
                raise ValueError(f"Invalid label in {split}")
    return names


def download_dataset():
    """Reuse a verified local copy, or download the pinned revision once."""
    manifest_path = DATASET_PATH / "source.json"
    source = {"dataset_id": DATASET_ID, "config": CONFIG, "revision": REVISION}
    if DATASET_PATH.exists():
        if not manifest_path.exists() or json.loads(manifest_path.read_text(encoding="utf-8")) != source:
            raise RuntimeError(f"Unverified or incomplete dataset at {DATASET_PATH}; inspect it before retrying.")
        dataset = load_from_disk(str(DATASET_PATH))
        validate_dataset(dataset)
    else:
        dataset = load_dataset(DATASET_ID, CONFIG, revision=REVISION)
        validate_dataset(dataset)
        dataset.save_to_disk(str(DATASET_PATH))
        manifest_path.write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
    print(f"GoEmotions (English): {DATASET_PATH}")
    print(dataset)
    return dataset


if __name__ == "__main__":
    download_dataset()
