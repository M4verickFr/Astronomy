import json
import os


def write_txt(path,error_data):
    with open(path,'a+') as f:
        f.write(error_data+'\r\n')
    f.close()


def read_txt():
    error_list = []
    with open('../../data/data_supernovae_error.txt','r') as f:
        for line in f:
            error_list.append(list(line.strip('\n').split(',')))
    return error_list


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False


def filter(path_err_data_txt,path_data_json):
    os.remove(path_err_data_txt)
    with open(path_data_json) as f:
        supernovae = json.load(f)
    for name,data in supernovae.items():
        ra = data.get('ra')
        decl = data.get('decl')
        ra_list = ra.split()
        decl_list = decl.split()
        if len(ra_list) !=2 or len(decl_list)!=2:
            if is_number(ra_list[0]) == False or is_number(decl_list[0]) == False:
                write_txt(path_err_data_txt,name)
        else:
            if is_number(ra_list[1]) == False or is_number(decl_list[1]) == False:
                write_txt(path_err_data_txt,name)
    f.close()


def get_url(path_data_json,path_url_txt):
    os.remove(path_url_txt)
    with open(path_data_json) as f:
        supernovae = json.load(f)
    error_names = read_txt()
    err_names = []
    for i in error_names:
        err_names.append(i[0])
    for name,data in supernovae.items():
        if name in err_names:
            None
        else:
            ra = data.get('ra')
            decl = data.get('decl')
            ra_list = ra.split()
            decl_list = decl.split()
            ra_new_list = ra_list[0]+'+'+ra_list[1]
            decl_new_list = decl_list[0] + '+' + decl_list[1]
            url = 'https://archive.stsci.edu/cgi-bin/dss_search?v=3&r='+ra_new_list+'&d='+decl_new_list+'&h=10&w=10&f=fits'
            write_txt(path_url_txt,url)
            print(url)




filter('../../data/data_supernovae_error.txt','../../data/table.json')
get_url('../../data/table.json','../../data/supernovae_url.txt')







