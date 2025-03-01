import logging
import os

class Logger:
    def __init__(self, log_file='dataset_merger.log'):
        self.logger = logging.getLogger('DatasetMergerLogger')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_changes(self, changes):
        for change in changes:
            self.log_info(change)

    def log_directory_scan(self, directory):
        self.log_info(f'Scanning directory: {directory}')

    def log_file_copy(self, source, destination):
        self.log_info(f'Copying file from {source} to {destination}')

    def log_file_rename(self, old_name, new_name):
        self.log_info(f'Renaming file from {old_name} to {new_name}')

    def log_conflict_resolution(self, conflict_details):
        self.log_info(f'Resolving conflict: {conflict_details}')

    def log_completion(self):
        self.log_info('Data merging process completed successfully.')


# Create a global logger instance
_logger_instance = None

def setup_logger(log_file='dataset_merger.log'):
    """
    Set up and return a global logger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = Logger(log_file)
    return _logger_instance


def get_logger():
    """
    Get the global logger instance, creating it if it doesn't exist
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = setup_logger()
    return _logger_instance