import nfl_data_py as nfl
import pandas as pd

def get_latest_season_qbs():
    # Fetch all available seasons
    all_rosters = nfl.import_seasonal_rosters(years=list(range(1999, 2025)))  # Fetch data from 1999 to now
    latest_season = all_rosters['season'].max()  # Get the most recent season
    
    # Fetch roster data for the latest season
    roster_data = nfl.import_seasonal_rosters(years=[latest_season])
    
    # Ensure column names are correct by checking available columns
    print("Available columns:", roster_data.columns.tolist())
    
    # Adjust column names based on actual dataset
    qb_columns = ['player_id', 'name', 'team', 'position', 'season']
    
    # Filter only quarterbacks (position = 'QB')
    if 'position' in roster_data.columns:
        qbs = roster_data[roster_data['position'] == 'QB']
    else:
        print("Column 'position' not found in dataset.")
        return pd.DataFrame()
    
    # Select relevant columns (ensure they exist)
    qbs = qbs[[col for col in qb_columns if col in qbs.columns]]
    
    return qbs

if __name__ == "__main__":
    qb_data = get_latest_season_qbs()
    
    # Save output to a CSV file
    qb_data.to_csv("latest_qbs.csv", index=False)
    
    print("QB data saved to latest_qbs.csv")
