import json
from pathlib import Path


DATASET_PATH = Path("data/raw/MoinSystems_AI_Public_Chatbot_RAG_Dataset_v2.jsonl")


def test_jsonl_file_exists():
    assert DATASET_PATH.exists(), "RAG JSONL dataset file not found"


def test_jsonl_records_are_valid():
    records = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)

            assert isinstance(record, dict), (
                f"Line {line_number} is not a JSON object"
            )

            records.append(record)

    assert len(records) == 99, (
        f"Expected 99 records, found {len(records)}"
    )


def test_required_fields_exist():
    required_fields = {
        "id",
        "title",
        "category",
        "content",
    }

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)

            missing = required_fields - record.keys()

            assert not missing, (
                f"Line {line_number} is missing fields: {missing}"
            )
def test_record_ids_are_unique():
    ids = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)
            ids.append(record["id"])

    assert len(ids) == len(set(ids)), "Duplicate record IDs found"

def test_content_is_not_empty():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)

            assert record["content"].strip(), (
                f"Empty content found on line {line_number}"
            )
def test_metadata_fields_are_present():
    required_metadata = {
        "category",
        "tags",
        "intents",
        "source_basis",
    }

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)

            missing = required_metadata - record.keys()

            assert not missing, (
                f"Line {line_number} is missing metadata fields: {missing}"
            )
from app.services.rag_ingestion import load_jsonl


def test_normalized_dataset_loads():
    records = load_jsonl()

    assert len(records) == 99

    for record in records:
        assert record["id"]
        assert record["content"]
        assert record["title"]    
from app.services.rag_ingestion import DATASET_VERSION


def test_dataset_version_is_defined():
    assert DATASET_VERSION == "v2"                            
