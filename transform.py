from datetime import datetime,timedelta
import pandas as pd
import datetime

def check_if_data_is_valid(df:pd.DataFrame)->bool:
    if df.empty:
        print("No songs downloaded.Finish execution.....")
        return False
    
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception ("duplicates present. Kindly deduplicate")
    if df.isnull().values.all():
        raise Exception("Null values available")
    
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0,minute=0,second=0,microsecond=0)

    timestamps = df['timestamps'].to_list()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp,'%Y-%m-%d') != yesterday:
            raise Exception("Not within 24 hours")