import os
import logging
from typing import List
from db.executor import AsyncDBExecutor
from validators.requests_ import IpDataRequest
from fastapi import APIRouter, HTTPException
from config.settings import (INPUT_FOLDER, RESULT_FOLDER,
                             ARCHIVE_FOLDER, WARNING_FOLDER,
                             RESULT_LOCAL_FOLDER, INTERVAL_DB_ERROR,
                             USERNAME, ROWS_QUANTITY)


def create_log_file():
    # log_path = f'{RESULT_FOLDER}/{USERNAME}.log'
    # with sftp.file(log_path, 'w') as log_file:
    #     logging.basicConfig(stream=log_file,
    #                         level=logging.INFO,
    #                         format='%(asctime)s - %(levelname)s - %(message)s',
    #                         force=True)
    if not os.path.exists(RESULT_LOCAL_FOLDER):
        os.makedirs(RESULT_LOCAL_FOLDER)
    logging.basicConfig(filename=f'{RESULT_LOCAL_FOLDER}/{USERNAME}.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        force=True)


ip_router = APIRouter(
    prefix="/ip",
)


@ip_router.post("/process", name="ips-process-endpoint")
async def ips_handler(ip_list: List[IpDataRequest]):
    """
    Main asynchronous function for handling a request with parameters:
    IP_DST, Port_DST, Date, Time, Provider
    """
    try:
        create_log_file()
        all_warning_numbers = set()
        warning_name_files = ''
        errors = ''
        results = []
        print(f'===============================================')
        logging.info(f'===============================================')
        print(ip_list)
        logging.info(ip_list)
        db_executor = AsyncDBExecutor()
        if await db_executor.connect_on():
            try:
                # DST_numbers_ls = []
                for ip_data in ip_list:
                    DST_numbers = await db_executor.execute(USERNAME, (
                        ip_data.IP_DST.__str__(), ip_data.Port_DST.__str__(),
                        ip_data.Date, ip_data.Time,
                        ip_data.Operator
                    ))
                    errors += db_executor.errors
                    db_executor.errors = ''
                    print(f'response: {DST_numbers}')
                    logging.info(f'response: {DST_numbers}')

                    # DST_numbers_ls.append(DST_numbers)

                    if DST_numbers != 'DB_ERROR':
                        status = 'Success'
                        message = 'Data processed successfully'
                    else:
                        status = 'ERROR_DB'
                        message = errors

                    if DST_numbers and next(iter(DST_numbers)) != 'ERROR':
                        warning_numbers = await db_executor.execute_check_numbers(DST_numbers)
                        errors += db_executor.errors
                        db_executor.errors = ''
                        if warning_numbers:
                            all_warning_numbers |= warning_numbers
                            print(f'!!! WARNING NUMBERS: {warning_numbers} !!!')
                            logging.info(f'!!! WARNING NUMBERS: {warning_numbers} !!!')

                    result = {
                        "IP_DST": str(ip_data.IP_DST),
                        "Port_DST": ip_data.Port_DST,
                        "Date": ip_data.Date,
                        "Time": ip_data.Time,
                        "Operator": ip_data.Operator,
                        "PhoneNumbers": DST_numbers,
                        "Status": status,
                        "Message": message,
                    }

                    results.append(result)

                return {"results": results}

            finally:
                await db_executor.connect_off()
                errors += db_executor.errors

    except Exception as e:
        print(f'Error processing request: {e}')
        logging.error(f'Error processing request: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
