"""CLI entrypoint for Gradio (Streamlit は CLI で起動する想定)."""
import argparse
import importlib
from config import cfg

def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ui",
        choices=["gradio", "streamlit"],
        default="gradio",          # ← run.sh から明示的に渡す
    )
    args = parser.parse_args()

    if args.ui == "gradio":
        ui = importlib.import_module("ui_gradio")
    else:
        # Streamlit CLI から呼ばれる際は fallback として import だけ行う
        ui = importlib.import_module("ui_streamlit")

    ui.launch()

if __name__ == "__main__":
    cli()
