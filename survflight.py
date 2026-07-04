import requests
import polars as pl
from datetime import datetime, timezone
import time


rotationdict = {}
turn_score = 0
valid_turns = 0.0
turn_totals = {}
while True:
    ##url = "https://api.airplanes.live/v2/point/52.3676/4.9041/100" around the netherlands
    url = "https://api.airplanes.live/v2/point/33.4484/-112.0740/100"  ##phoenix area
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    print("total:", data.get("total"))

    commonairliners =    "KLM", "RYR", "EZY", "EWG", "BEL", "DAL", "UAL", "BAW", "QTR", "UAE", "CPA", "SAS", "IBE", "TAP", "THY", "ACA","AUA", "WZZ", "TRA", "TOM", "FDX"


    pl.Config.set_tbl_cols(-1)
    pl.Config.set_tbl_rows(-1)
    pl.Config.set_tbl_width_chars(2000)
    pl.Config.set_fmt_str_lengths(2000)

    turning_rates = []


    rows = [{

            "hex": ac.get("hex"),
            "flight": ac.get("flight"),
            "squawk": ac.get("squawk"),
            "registry": ac.get("r"),
            "type": ac.get("t"),
            "desc": ac.get("desc"),
            "alt_baro": ac.get("alt_baro"),
            "gs": ac.get("gs"),
            "mach": ac.get("mach"),
            "track": ac.get("track"),
            "track_rate": ac.get("track_rate"),
            "baro_rate": ac.get("baro_rate"),
            "latitude": ac.get("lat"),
            "longitude": ac.get("lon"),

            "seen_pos": ac.get("seen_pos"),
            "seen": ac.get("seen"),

        }
        for ac in data.get("ac", [])


    ]

    df = pl.DataFrame(rows)

    df = df.filter(



            (~pl.col("flight").str.contains("KLM|RYR|EZY|EWG|BEL|DAL|UAL|AAL|ACA|BAW|QTR|UAE|CPA|SAS|IBE|AFR|DLH|TAP|THY|TRA|TUI|CFG|EXS|JAF|TOM|FDX|UPS|OCN").fill_null(False))
        ).with_columns(
            pl.col("alt_baro").cast(pl.Int64, strict=False),
            pl.col("alt_baro").rank().alias("alt_rank"),
            pl.col("gs").rank().alias("gs_rank")

        ).with_columns(
            ((pl.col("alt_rank") + pl.col("gs_rank")) / 2).alias("score")
        ).sort("score", descending=False)


    df = df.with_columns(pl.when(pl.col("track") > 300).then(pl.lit("jee")).otherwise(pl.lit(None)))




    for hex, value in zip(df["hex"], df["track"]): ## iterate over both of these integers and make hex the name of the list and make track the values monitored in that list.
        if hex not in rotationdict: ## checks if aircraft hex isn't already a list
            rotationdict[hex] = []       ## assigns the aircraft hex to rotationdict as a list

        if hex not in turn_totals: ##creates the entry hex for a new aircraft
            turn_totals[hex] = 0.0 ##assigns it zero because we dont know how much the aircraft turned yet


        previous_tracks = rotationdict[hex] ##assigns the current airplanes location dictionary to the previous_hex variable

        if previous_tracks and value is not None and previous_tracks[-1] is not None:
            prev_track = previous_tracks[-1]
            turning_rate = abs(((value - prev_track + 180) % 360) - 180) ##calculates the difference between the last and second to last turns.
            turn_totals[hex] += turning_rate ##summing the differences so we can eventually rank them over time, how bigger the number how more turns the aircraft did in that time.
        else:
            turning_rate = None
        rotationdict[hex].append(value) ## puts that value at that hex into the list


        turning_rates.append(turn_totals[hex])

    df = df.with_columns(
        pl.Series("turningrate", turning_rates, dtype=pl.Float64)
    )






    print(df)
    print(rotationdict)
    time.sleep(2)

