import pandas as pd


def export_to_csv(info: dict, filename: str) -> None:
    data_frame = pd.DataFrame(info)
    data_frame.to_csv(filename, encoding='utf-8', index=False)
