import os
import shutil
from pathlib import Path
from utils.logger import get_logger

def copy_file(src, dst):
    logger = get_logger()
    try:
        shutil.copy2(src, dst)
        logger.log_file_copy(src, dst)
    except Exception as e:
        logger.log_error(f"Error copying file from {src} to {dst}: {e}")

def copy_folder(src, dst):
    logger = get_logger()
    try:
        shutil.copytree(src, dst)
        logger.log_info(f"Copied folder from {src} to {dst}")
    except Exception as e:
        logger.log_error(f"Error copying folder from {src} to {dst}: {e}")

def rename_folder(src, new_name):
    logger = get_logger()
    try:
        os.rename(src, new_name)
        logger.log_file_rename(src, new_name)
    except Exception as e:
        logger.log_error(f"Error renaming folder {src} to {new_name}: {e}")

def delete_file(file_path):
    logger = get_logger()
    try:
        os.remove(file_path)
        logger.log_info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.log_error(f"Error deleting file {file_path}: {e}")

def delete_folder(folder_path):
    logger = get_logger()
    try:
        shutil.rmtree(folder_path)
        logger.log_info(f"Deleted folder: {folder_path}")
    except Exception as e:
        logger.log_error(f"Error deleting folder {folder_path}: {e}")