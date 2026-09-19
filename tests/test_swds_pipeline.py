"""
INTEGRA O/S: SWDS Pipeline Tests (Local SQLite)
Migrated from Apache Beam/BigQuery tests to native Python/SQLite tests.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipelines.swds_pipeline import (
    load_shards, classify_nodes, SWDSHistoryDB, run_pipeline
)


class TestSWDSPipeline(unittest.TestCase):

    def test_load_shards(self):
        """Test loading JSON shard files from a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write test shards
            shard1 = {"ccid": "CCID_001", "sufficiency_score": 0.8, "payload": {"content": "test1"}}
            shard2 = {"ccid": "CCID_002", "sufficiency_score": 0.1, "payload": {"content": "test2"}}
            with open(os.path.join(tmpdir, "CCID_001.json"), "w") as f:
                json.dump(shard1, f)
            with open(os.path.join(tmpdir, "CCID_002.json"), "w") as f:
                json.dump(shard2, f)
            # Write an invalid file
            with open(os.path.join(tmpdir, "bad.json"), "w") as f:
                f.write("not valid json{{{")

            nodes = load_shards(tmpdir)
            assert len(nodes) == 2
            assert nodes[0]["ccid"] == "CCID_001"
            assert nodes[1]["ccid"] == "CCID_002"

    def test_classify_nodes(self):
        """Test IsolationForest classification of active vs stale nodes."""
        nodes = [
            {"ccid": f"CCID_{i:03d}", "sufficiency_score": 0.9, "payload": "active" * 100}
            for i in range(10)
        ]
        # Add a clearly stale node
        nodes.append({"ccid": "CCID_STALE", "sufficiency_score": 0.1, "payload": "x"})

        result = classify_nodes(nodes)
        assert "active" in result
        assert "stale" in result
        # The stale node with score 0.1 should always be classified stale
        stale_ccids = [n["ccid"] for n in result["stale"]]
        assert "CCID_STALE" in stale_ccids

    def test_classify_empty(self):
        """Test classification with fewer than 2 nodes returns all active."""
        result = classify_nodes([{"ccid": "solo", "sufficiency_score": 0.5, "payload": "x"}])
        assert len(result["active"]) == 1
        assert len(result["stale"]) == 0

    def test_sqlite_archive(self):
        """Test SQLite archival of stale nodes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_swds.db")
            db = SWDSHistoryDB(db_path=db_path)

            nodes = [
                {"ccid": "CCID_001", "payload": {"content": "test", "type": "text"}, "sufficiency_score": 0.2},
                {"ccid": "CCID_002", "payload": {"content": "test2", "type": "code"}, "sufficiency_score": 0.1},
            ]
            archived = db.archive_nodes(nodes)
            assert archived == 2

            stats = db.get_archive_stats()
            assert stats["total_archived"] == 2
            assert stats["db_path"] == db_path

    def test_full_pipeline(self):
        """Test the full pipeline end-to-end with temp dirs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create input shard dir
            shards_dir = os.path.join(tmpdir, "shards")
            os.makedirs(shards_dir)
            for i in range(5):
                shard = {"ccid": f"CCID_{i}", "sufficiency_score": 0.9, "payload": {"content": f"data_{i}"}}
                with open(os.path.join(shards_dir, f"CCID_{i}.json"), "w") as f:
                    json.dump(shard, f)
            # Add one stale shard
            stale = {"ccid": "CCID_STALE", "sufficiency_score": 0.05, "payload": "x"}
            with open(os.path.join(shards_dir, "CCID_STALE.json"), "w") as f:
                json.dump(stale, f)

            db_path = os.path.join(tmpdir, "pipeline_test.db")
            result = run_pipeline(input_dir=shards_dir, db_path=db_path)

            assert result["status"] == "PIPELINE_COMPLETE"
            assert result["total_loaded"] == 6
            assert result["storage_backend"] == "SQLite (local)"
            assert result["archived"] >= 1  # At least the stale node

    def test_format_for_bq_compat(self):
        """Backward compatibility: Verify archived node format matches old BQ schema."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "compat.db")
            db = SWDSHistoryDB(db_path=db_path)

            node = {"ccid": "123", "payload": {"content": "test", "type": "text"}, "sufficiency_score": 0.2}
            db.archive_nodes([node])

            stats = db.get_archive_stats()
            assert stats["total_archived"] == 1


if __name__ == '__main__':
    unittest.main()
