from sys import getdefaultencoding
from RPA.Excel.Files import Files
import json, config, getdata, re, os, datetime, shutil
from RPA.PDF import PDF

xlFiles = Files()

#create output folder
def create_output_folder():
    print(os.path.join('.', config.path_to_save))
    try:
        if not os.path.exists(os.path.join('.', config.path_to_save)):
            os.makedirs(os.path.join('.', config.path_to_save))
            
        else:
            shutil.rmtree(os.path.join('.', config.path_to_save))
            os.makedirs(os.path.join('.', config.path_to_save))
    except Exception as e:
        print('Unexpected error in create_output_folder. Exception: {e}')

#Format spendings
def format_spendings(spending):
    if(spending > 0):
        if(spending  >= 10000):
            spending = f'${round(spending/1000, 0)}B'
        elif(spending >= 1000):
            spending = f'${round(spending/1000, 1)}B'
        elif(spending >= 100):
            spending = f'${round(spending, 0)}M'
        elif(spending >= 1):
            spending = f'${round(spending, 1)}M'
        else:
            spending = f'${round(spending * 100, 0)}K'
    elif(spending is None):
        spending = '--'
    return spending

def add_data_to_rows(json_data, isagencyinfo: bool, rows):
    data = json.loads(json_data)
    if isagencyinfo:
        for i in data['result']:
            rows.append([i['UII'], i['bureauName'], i['investmentTitle'], i['totalCySpending'], i['investmentType'], i['cioRating'], i['numberOfProjects']])
    else:
        for i in data['result']:
            rows.append([i['agencyName'], format_spendings(i['totalSpendingCY'])])

def get_agency_code(agencies_info):
    data = json.loads(agencies_info)
    agency_code = ''
    for i in data['result']:
        if i['agencyName'] == config.agency_name:
            agency_code = i['agencyCode']
            break
    return agency_code

def write_agencies_info_file(path_to_save, agencies_info, ):
    rows = [['Agency Name', 'Total FY2021 Spending']]
    add_data_to_rows(agencies_info, False, rows)
    xlFiles.create_workbook(path_to_save, fmt='xlsx')
    xlFiles.create_worksheet(name='Agencies')
    remove_default_sheet()
    xlFiles.append_rows_to_worksheet(rows, 'Agencies')
    xlFiles.save_workbook(path_to_save)
    xlFiles.close_workbook()

def write_agency_info(path_to_save, agency_info):
    rows = [['UII', 'Bureau', 'Investment Title', 'Total FY2021 Spending ($M)', 'Type', 'CIO Rating', '# of projects']]
    add_data_to_rows(agency_info, True, rows)
    xlFiles.open_workbook(path_to_save)
    xlFiles.create_worksheet(name=config.agency_name)
    xlFiles.append_rows_to_worksheet(rows, config.agency_name)
    xlFiles.save_workbook(path_to_save)
    xlFiles.close_workbook()
    return rows

def remove_default_sheet():
    try:
        xlFiles.remove_worksheet('Sheet')
    except Exception as e:
        print(f'Remove default sheet exception: {e}')

def download_PFDs(agency_info, cookies_and_headers):
    data = json.loads(agency_info)
    for i in data['result']:
        if not (i['businessCaseId'] is None):
            getdata.get_PDF(cookies_and_headers[0], cookies_and_headers[1], i['UII'])

def get_PDF_data(agencyinfo, path_to_save):
    rows = [['File Name', 'Name of Investments comparsion result', 'UII comparsion result']]
    pdf = PDF()
    for file in [f for f in os.listdir(f'.\{config.path_to_save}') if f.endswith('.pdf')]:
        row = []
        try:
            row.append(os.path.join('.\output', file))
            pdf_text = pdf.get_text_from_pdf(os.path.join('.\output', file))
            name = re.search(r'1. Name of this Investment: (.*?)2.', str(pdf_text)).group(1).strip()
            uii = re.search(r'2. Unique Investment Identifier \(UII\):(.*?)Section B:', str(pdf_text)).group(1).strip()

            if name in (item for sublist in agencyinfo for item in sublist):
                row.append('True')
            else:
                row.append('False')
            if uii in (item for sublist in agencyinfo for item in sublist):
                row.append('True')
            else:
                row.append('False')
        except Exception as e:
            print(f'Error occured when trying to read the file: {file}. Exception: {e}')
        rows.append(row)
    write_PDFs_info(path_to_save, rows)

def write_PDFs_info(path_to_save, rows):
    xlFiles.open_workbook(path_to_save)
    xlFiles.create_worksheet(name='Data comparsion')
    xlFiles.append_rows_to_worksheet(rows, 'Data comparsion')
    xlFiles.save_workbook(path_to_save)
    xlFiles.close_workbook()