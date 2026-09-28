from pathlib import Path

message = Path("message.txt").read_text(encoding="utf-8")
keep = Path("KEEP.txt").read_text(encoding="utf-8")
assert message == "safe release\n", repr(message)
assert keep == "keep me\n", repr(keep)
print("fixture check passed")
