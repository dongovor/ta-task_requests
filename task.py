import getdata, config, time, os, datetime, utils



def main():
    try:
        report_name = f'.\{config.path_to_save}\itdashboardgov_{datetime.datetime.now().strftime("%m-%d-%Y %H.%M.%S %p")}.xlsx'
        utils.create_output_folder()
        process_started = time.time()
        print('Process started')
        print('Prepare cookies and headers')
        cookies_and_headers = getdata.get_cookies_and_headers()
        print('Collecting agencies spendings info.')
        agenciesData = getdata.collect_data(cookies_and_headers[0], cookies_and_headers[1])
        print('All necessary agencies info collected.')
        print('Writing agencies spednings to excel file.')
        utils.write_agencies_info_file(report_name, agenciesData)
        print('Spending info successfully written.')
        agencyInfo = getdata.get_agency_info(cookies_and_headers[0], cookies_and_headers[1], agenciesData)
        print(f"{config.agency_name} information successfully extracted.")
        print(f'Writing {config.agency_name} info to excel file.')
        agencyInfoRows = utils.write_agency_info(report_name, agencyInfo)
        print(f'{config.agency_name} info successfully written.')
        utils.download_PFDs(agencyInfo, cookies_and_headers)
        print('All PDF files successfully downloaded.')
        utils.get_PDF_data(agencyInfoRows, report_name)
    except Exception as e:
        print(e)
    finally:
        pass

if __name__ == "__main__":
    main()