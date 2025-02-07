import nfl_data_py as nfl
import pandas as pd

def get_latest_qb_season_aggregate():
    # 1. Identify the latest season from the available roster data
    all_rosters = nfl.import_seasonal_rosters(years=list(range(1999, 2025)))
    latest_season = all_rosters["season"].max()
    print(f"Detected latest season as: {latest_season}")

    # 2. Load rosters & weekly data for that season
    rosters_data = nfl.import_seasonal_rosters(years=[latest_season])
    weekly_data = nfl.import_weekly_data(years=[latest_season])

    # 3. Merge rosters & weekly data on [player_id, season]
    merged_data = pd.merge(
        weekly_data,
        rosters_data,
        on=["player_id", "season"],
        how="left",
        suffixes=("_wk", "_r")
    )

    # 4. Filter for QBs using whichever position column exists
    if "position_wk" in merged_data.columns:
        qbs = merged_data[merged_data["position_wk"] == "QB"]
    else:
        qbs = merged_data[merged_data["position_r"] == "QB"]

    # 5. Group by player & season, aggregate passing yards, TDs, and INTs
    #    (Adjust column names if your environment uses different names, e.g. 'passing_yards' -> 'pass_yds')
    agg_cols = {
        "passing_yards": "sum",
        "passing_tds": "sum",
        "interceptions": "sum"
    }
    qb_agg = qbs.groupby(["player_id", "season"], dropna=False).agg(agg_cols).reset_index()

    # 6. Calculate TD-to-INT ratio (handling divide-by-zero)
    def td_int_ratio(tds, ints):
        if ints == 0:
            return None  # or float('inf') if you'd rather show 'infinity'
        return round(tds / ints, 2)
    
    qb_agg["td_to_int_ratio"] = qb_agg.apply(
        lambda row: td_int_ratio(row["passing_tds"], row["interceptions"]),
        axis=1
    )

    # 7. Merge aggregated stats back with rosters to include player names/teams
    #    (the rosters might store 'player_name', 'team', 'position'—adjust if needed)
    final_qbs = pd.merge(
        qb_agg,
        rosters_data[["player_id", "player_name", "team", "position"]],
        on="player_id",
        how="left"
    ).drop_duplicates()

    # 8. Output final aggregated QB stats to CSV
    final_qbs.to_csv("latest_qbs_aggregate.csv", index=False)
    return final_qbs

if __name__ == "__main__":
    df_qb_stats = get_latest_qb_season_aggregate()
    print(f"Saved aggregated QB stats to latest_qbs_aggregate.csv")
    print(f"Rows: {len(df_qb_stats)}")
    print("Preview:")
    print(df_qb_stats.head(10))
