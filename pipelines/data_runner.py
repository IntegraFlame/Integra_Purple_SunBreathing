"""
INTEGRA O/S: Data Runner Pipeline Stub
Provides MCP stdio interface for 'inspect_schema' and 'run_pipeline_query'.
"""
import sys
import json

def main():
    # Stub implementation to prevent module loading errors
    # during SDK harness initialization.
    for line in sys.stdin:
        try:
            req = json.loads(line)
            # Just echo back an error that this is a stub
            print(json.dumps({"error": "Data runner pipeline not fully implemented"}))
            sys.stdout.flush()
        except Exception:
            pass

if __name__ == "__main__":
    main()
