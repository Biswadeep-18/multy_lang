try:
    from duckduckgo_search import DDGS
    print("duckduckgo_search is installed and importable")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Exception: {e}")
