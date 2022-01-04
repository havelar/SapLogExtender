from application.src.formatResponse import format_response
from application.src.S3Object import getObject, putObject
from application.src.RouteError import RouteError
from application.src.chunks import chunks
from application.src.table import Table
from application.src.io import buildZip

import traceback
import json
import re

colsRgx = re.compile(r"(.+?)\s{2,}")

def main(event, context):
    try:
        params = event["body"] if "body" in event.keys() else event
        if not isinstance(params, dict):
            params = json.loads(params)

        file_name = params["file_name"]

        file_text, file_name = getObject(file_name)
        
        splitted_tables = file_text.split('Log created on')

        ## Top File Header
        file_header = splitted_tables.pop(0)
        
        ## Build headers
        headers = splitted_tables[0].split('\n', 6)[:6]
        date = headers[0].strip()

        information = headers[2].split()
        if len(information) == 1: information = ''
        else: information = information[-1]
        
        warnings = headers[3].split()
        if len(warnings) == 1: warnings = ''
        else: warnings = warnings[-1]
        
        errors = headers[4].split()
        if len(errors) == 1: errors = ''
        else: errors = errors[-1]
        
        totals = headers[5].split()
        if len(totals) == 1: totals = ''
        else: totals = totals[-1]

        headers = {
            'date': date,
            'information': information,
            'warnings': warnings,
            'errors': errors,
            'totals': totals
        }
        
        every_tables = []
        for table_ind, table in enumerate(splitted_tables):
            table_lines = table.split('\n')
            
            columns = [
                'Exc.', 'Msg.typ', 'Application Area', 'MsgNo', 'Number', 'Numer.',
                'Order', 'Seq.', 'OpAc',
                'Message Text'
            ]
            
            ## Table values start at line 12: '|---- ...|'
            rows = chunks(table_lines[12:], 3) # A single row is divided in 3 rows
            
            every_values = []
            for row in rows:
                row = ''.join(row).replace('|', '')
                values = [v.group(1) for v in colsRgx.finditer(row)]
                if values:
                    values[0] = ''
                    values.insert(7, '')
                    values.insert(7, '')
                    every_values.append(values)
                
            if table_ind == len(splitted_tables)-1:
                every_values = every_values[:-2]
                    
            table = Table(headers, columns, every_values)
            every_tables.append(table)

        zipFileIO = buildZip(file_header, every_tables, file_name)

        presigned_url = putObject(zipFileIO, file_name)

        response = format_response(
            {
                'presigned_url': presigned_url
            },
            status_code=200
        )

    except RouteError as e:
        response = format_response({'message': e.message}, e.status_code)

    except Exception as e:
        error ={
            "exception": str(e),
            "error": traceback.format_exc(),
            "function": 'addAnswer',
            "event": event
        }
        print(error)
        # Send to SNS
        response = format_response({'message': 'Something went wrong.', 'error': error}, 500)

    finally:
        return response