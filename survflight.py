import requests
import polars as pl


##url = "https://api.airplanes.live/v2/point/52.3676/4.9041/100"
url = "https://api.airplanes.live/v2/point/33.4484/-112.0740/100"
resp = requests.get(url, timeout=10)
resp.raise_for_status()

data = resp.json()
print("total:", data.get("total"))

commonairliners =    "KLM", "RYR", "EZY", "EWG", "BEL", "DAL", "UAL", "BAW", "QTR", "UAE", "CPA", "SAS", "IBE", "TAP", "THY", "ACA","AUA", "WZZ", "TRA", "TOM", "FDX"


pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)
pl.Config.set_tbl_width_chars(2000)
pl.Config.set_fmt_str_lengths(2000)





rows = [{

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



print(df)