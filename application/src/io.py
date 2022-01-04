from application.src.Zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO

def buildZip(header:str, tables:list, file_name: str):
    '''
    Receive a string Header and a list of Tables, so it appends on bottom of each.
    '''
    # text = header
    # for t_ind, table in enumerate(tables):
    #     print(t_ind)
    #     text += table.tab()

    
    final_table = tables.pop(0)
    for table in tables:
        final_table.values.extend(table.values)

    text = header + final_table.tab()

    in_memory = BytesIO()
    zf = ZipFile(in_memory, mode="w", compression=ZIP_DEFLATED)
    zf.writestr(file_name, text)
    zf.close()

    return in_memory

