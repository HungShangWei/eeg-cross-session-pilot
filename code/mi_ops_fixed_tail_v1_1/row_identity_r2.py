"""Shared canonical row identity; no dependency on orchestration versions."""
def row_id(key):return ":".join(str(v) for v in key)
