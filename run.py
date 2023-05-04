import pandas as pd

import american_carbon
import gold_standard
import verra
import methodologies

providers = [verra, gold_standard, american_carbon]

FINAL = "data/offsets.csv"


def merge_and_save():
    out = []
    for p in providers:
        out.append(p.merge())

    out = pd.concat(out)
    out.to_csv(FINAL, index=False)
    # out.to_json("data/offset.json", orient="records")


def run_all():
    for p in providers:
        p.run()

    merge_and_save()

    methodologies.run()


if __name__ == "__main__":
    run_all()
