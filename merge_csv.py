import csv
import futsu.csv
import futsu.fs
import os.path
import re
import tempfile

csv_path_list = futsu.fs.find_file('manulife_alpha_price/output')
csv_path_list = list(filter(lambda i:i.endswith('.csv'), csv_path_list))

# copy from futsu.csv.read_csv, and mod
def read_csv(fn):
    with tempfile.TemporaryDirectory() as tdir:
        tfn = os.path.join(tdir,'HIWHQBQB')

        bs = futsu.fs.file_to_bytes(fn)
        if bs.startswith(b'\xef\xbb\xbf'):
          bs = bs[3:]
        futsu.fs.bytes_to_file(tfn,bs)
        
        col_name_list = None
        ret = []
        with open(tfn, 'r') as fin:
            for line in csv.reader(fin):
                if len(line) == 0: continue
                if col_name_list is None:
                    col_name_list = list(line)
                else:
                    if((len(col_name_list) == 1) and (len(line) == 0)):
                        line = ['']
                    assert(len(line) == len(col_name_list))
                    ret.append({col_name_list[i]: line[i].strip() for i in range(len(col_name_list))})
        return ret, col_name_list

# Fuck Manulife, change date format from yyyy/mm/dd to mm/dd/yyyy
def conv_date(txt):
    #print(f'HTGXPJCV txt={txt}')

    # output format, yyyy-mm-dd
    m = re.fullmatch('(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)',txt)
    if m is not None:
        return txt

    # input format, mm/dd/yyyy
    m = re.fullmatch('(\\d\\d)/(\\d\\d)/(\\d\\d\\d\\d)',txt)
    if m is not None:
        return ''+m.group(3)+'-'+m.group(1)+'-'+m.group(2)

    # old format, yyyy/mm/dd
    m = re.fullmatch('(\\d\\d\\d\\d)/(\\d\\d)/(\\d\\d)',txt)
    if m is not None:
        return ''+m.group(1)+'-'+m.group(2)+'-'+m.group(3)

    print(f'Err: RCCHXVCH txt={txt}')
    assert(False)

for csv_path in csv_path_list:
    _, csv_fn = os.path.split(csv_path)
    print(csv_fn)
    last_csv_path = os.path.join('last_csv', csv_fn)
    target_csv_path = os.path.join('manulife_alpha_price_csv', 'csv', csv_fn)
    
    if futsu.fs.is_exist(last_csv_path):
        new_data_list,_ = read_csv(csv_path)
        last_data_list,_ = read_csv(last_csv_path)
        
        new_data_list = filter(lambda i:len(i['Date'])>0,new_data_list)
        new_data_list = list(new_data_list)

        last_data_list = filter(lambda i:len(i['Date'])>0,last_data_list)
        last_data_list = list(last_data_list)
        
        for data in new_data_list:
            data['Date'] = conv_date(data['Date'])

        for data in last_data_list:
            data['Date'] = conv_date(data['Date'])
            if 'Investment choice name' not in data:
                #print(data)
                #for k,v in data.items():
                #  print(f'k={k}, len(k)={len(k)}')
                assert('Name of Investment Choice' in data)
                data['Investment choice name'] = data['Name of Investment Choice']
            if 'NAV / unit' not in data:
                assert('Purchase Price' in data)
                data['NAV / unit'] = data['Purchase Price']
        
        new_date_to_data_dict = {i['Date']: i for i in new_data_list}
        date_to_data_dict = {i['Date']: i for i in last_data_list}
        
        date_to_data_dict.update(new_date_to_data_dict)
        
        data_list = list(date_to_data_dict.values())
        
        futsu.csv.write_csv(
            target_csv_path,
            data_list,
            ['Investment choice name','Date','Currency','NAV / unit'],
            ['Date']
        )
    else:
        new_data_list,_ = read_csv(csv_path)

        for data in new_data_list:
            data['Date'] = conv_date(data['Date'])

        futsu.csv.write_csv(
            target_csv_path,
            data_list,
            ['Investment choice name','Date','Currency','NAV / unit'],
            ['Date']
        )
