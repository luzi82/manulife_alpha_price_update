import csv
import futsu.csv
import futsu.fs
import os.path
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

for csv_path in csv_path_list:
    _, csv_fn = os.path.split(csv_path)
    print(csv_fn)
    last_csv_path = os.path.join('last_csv', csv_fn)
    target_csv_path = os.path.join('manulife_alpha_price_csv', 'csv', csv_fn)
    
    if futsu.fs.is_exist(last_csv_path):
        new_data_list,_ = read_csv(csv_path)
        last_data_list,_ = read_csv(last_csv_path)
        
        new_date_to_data_dict = {i['Date']: i for i in new_data_list}
        date_to_data_dict = {i['Date']: i for i in last_data_list}
        
        date_to_data_dict.update(new_date_to_data_dict)
        
        data_list = list(date_to_data_dict.values())
        
        futsu.csv.write_csv(
            target_csv_path,
            data_list,
            ['Name of Investment Choice','Date','Currency','Purchase Price','Unit Sell Price'],
            ['Date']
        )
    else:
        futsu.fs.cp(target_csv_path, csv_path)
