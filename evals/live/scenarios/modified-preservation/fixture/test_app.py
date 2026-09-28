import unittest

from app import build_record


class RecordContractTests(unittest.TestCase):
    def test_record_contract(self):
        record = build_record()
        self.assertEqual("r-1", record["id"])
        self.assertEqual("Ada", record["name"])
        self.assertEqual("ready", record["status"])
        self.assertEqual(["read", "write"], record["permissions"])


if __name__ == "__main__":
    unittest.main()
