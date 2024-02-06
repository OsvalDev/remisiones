import pandas as pd
from io import BytesIO

def getPdf(data, headers):    
    df = pd.DataFrame(data, columns = headers)
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    return excel_data.getvalue()