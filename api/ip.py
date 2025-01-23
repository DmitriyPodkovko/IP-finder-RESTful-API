import os
import platform
import subprocess
from datetime import datetime
import uuid
import logging
import shutil
from typing import List
from db.executor import AsyncDBExecutor
from validators.requests_ import IpDataRequest
from fastapi import APIRouter, HTTPException
from config.settings import (SHARE_USERNAME, SHARE_PASSWORD,
                             MOUNT_POINT_LOG, LOG_FOLDER,
                             MOUNT_POINT_REQUEST, REQUEST_FOLDER,
                             MOUNT_POINT_WARNING, WARNING_FOLDER,
                             RESULT_LOCAL_FOLDER, USERNAME)


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


def mount_network_folder(mount_point, folder):
    """
    Mounts a network folder if it is not already mounted.
    """
    try:
        # Create a mount point if it doesn't exist
        if not os.path.exists(mount_point):
            os.makedirs(mount_point, exist_ok=True)
            print(f"Created mount point directory: {mount_point}")
            logging.info(f"Created mount point directory: {mount_point}")
        # Check if the folder is already mounted
        if not os.path.ismount(mount_point):
            print(f"Mounting network folder: {folder} to {mount_point}")
            logging.info(f"Mounting network folder: {folder} to {mount_point}")

            current_os = platform.system()
            if current_os == "Linux":  # For Linux
                try:
                    subprocess.run([
                        'mount', '-t', 'cifs', folder, str(mount_point),
                        '-o', f'username={SHARE_USERNAME},password={SHARE_PASSWORD},rw'
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Failed to mount on Linux: {e}")
                    logging.error(f"Failed to mount on Linux: {e}")
                    raise
            elif current_os == "Darwin":  # For macOS
                try:
                    subprocess.run([
                        'mount_smbfs', folder, str(mount_point)
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Failed to mount on macOS: {e}")
                    logging.error(f"Failed to mount on macOS: {e}")
                    raise
            else:
                raise OSError(f"Unsupported OS: {current_os}")

            print(f"Mounted network folder: {folder} to {mount_point}")
            logging.info(f"Mounted network folder: {folder} to {mount_point}")
        else:
            print(f"Network folder already mounted: {mount_point}")
            logging.info(f"Network folder already mounted: {mount_point}")
    except Exception as e:
        print(f"Error mounting network folder: {e}")
        logging.error(f"Error mounting network folder: {e}")
        raise


def move_file_with_unique_name(src_file, dest_folder):
    """
    Moves a file to the destination folder with a unique name
    if a file with the same name exists.
    """
    try:
        # Get file name from source path
        base_name = os.path.basename(src_file)
        # Destination path
        dest_path = os.path.join(dest_folder, base_name)
        # If the file already exists, create a unique name
        if os.path.exists(dest_path):
            base_name_without_ext, ext = os.path.splitext(base_name)
            # Generate a 5-character unique identifier
            unique_id = uuid.uuid4().hex[:5]
            unique_name = f'{base_name_without_ext}_{unique_id}{ext}'
            dest_path = os.path.join(dest_folder, unique_name)
        shutil.move(src_file, dest_path)
        print(f'Moved file: {src_file} to {dest_path}')
        logging.info(f'Moved file: {src_file} to {dest_path}')
        return dest_path
    except Exception as e:
        print(f"Error moving file: {e}")
        logging.error(f"Error moving file: {e}")
        raise


ip_router = APIRouter(
    prefix="/ip",
)


@ip_router.post("/process", name="ips-process-endpoint")
async def ips_handler(ip_list: List[IpDataRequest]):
    """
    Main asynchronous function for handling a request with parameters:
    Otbor, IP_DST, Port_DST, Date, Time, Provider
    """
    try:
        create_log_file()
        errors = ''
        results = []
        print(f'===============================================')
        logging.info(f'===============================================')
        print(ip_list)
        logging.info(ip_list)
        db_executor = AsyncDBExecutor()
        if await db_executor.connect_on():
            try:
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

                    # Check DST_numbers
                    if DST_numbers and next(iter(DST_numbers)) != 'ERROR':
                        warning_numbers = await db_executor.execute_check_numbers(DST_numbers)
                        errors += db_executor.errors
                        db_executor.errors = ''
                        if warning_numbers:
                            print(f'!!! WARNING NUMBERS: {warning_numbers} !!!')
                            logging.info(f'!!! WARNING NUMBERS: {warning_numbers} !!!')
                            # Removing numbers from DST_numbers that were caught in warning_numbers
                            DST_numbers = [num for num in DST_numbers if num not in warning_numbers]
                            print(f'Clean numbers: {DST_numbers}')
                            logging.info(f'Clean numbers: {DST_numbers}')
                            today = datetime.now().strftime('%Y_%m_%d')
                            warning_file_name = f'{today}_warning_numbers.txt'
                            warning_file = os.path.join(RESULT_LOCAL_FOLDER, warning_file_name)
                            with open(warning_file, 'a') as file:
                                file.write(f'Otbor: {ip_data.Otbor}, '
                                           f'IP DST: {ip_data.IP_DST}, '
                                           f'Port DST: {ip_data.Port_DST}, '
                                           f'Date: {ip_data.Date}, '
                                           f'Time: {ip_data.Time}, '
                                           f'Provider: {ip_data.Operator}, ' +
                                           ' '.join(map(str, warning_numbers)) + '\n')
                                print(f'Warning numbers are saved in: {warning_file}')
                                logging.info(f'Warning numbers are saved in: {warning_file}')
                            mount_network_folder(MOUNT_POINT_WARNING, WARNING_FOLDER)
                            move_file_with_unique_name(warning_file, MOUNT_POINT_WARNING)

                    result = {
                        "Otbor": ip_data.Otbor,
                        "IP_DST": ip_data.IP_DST.__str__(),
                        "Port_DST": ip_data.Port_DST,
                        "Date": ip_data.Date,
                        "Time": ip_data.Time,
                        "Operator": ip_data.Operator,
                        "PhoneNumbers": DST_numbers,
                        "Status": "Success" if DST_numbers != "ERROR"
                        else "ERROR",
                        "Message": "Data processed successfully" if DST_numbers != "ERROR"
                        else errors,
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
    finally:
        mount_network_folder(MOUNT_POINT_LOG, LOG_FOLDER)
        move_file_with_unique_name(f'{RESULT_LOCAL_FOLDER}/{USERNAME}.log', MOUNT_POINT_LOG)
