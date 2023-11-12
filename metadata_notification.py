import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MetadataManager:
    """
    Manages metadata associated with different tables.
    """
    """
    This class manages metadata associated with different tables.
    """

    def __init__(self):
        """
        Initialize the MetadataManager with an empty metadata dictionary.
        """
        logging.info("Initializing MetadataManager.")
        self.metadata = {}

    def add_metadata(self, table_name, description, source=None, additional_info=None):
        """
        Add metadata for a given table.

        Args:
            table_name (str): Name of the table to add metadata for.
            description (str): Description of the table.
            source (str, optional): Source of the table data.
            additional_info (str, optional): Any additional information related to the table.
        """
        """
        Add metadata for a given table.
        
        :param table_name: Name of the table to add metadata for.
        :param description: Description of the table.
        :param source: Source of the table data.
        :param additional_info: Any additional information related to the table.
        """
        logging.info(f"Adding metadata for table: {table_name}")
        self.metadata[table_name] = {
            "description": description,
            "source": source,
            "additional_info": additional_info
        }

    def get_metadata(self, table_name):
        """
        Retrieve metadata for a given table, if it exists.
        
        :param table_name: Name of the table to retrieve metadata for.
        :return: Metadata dictionary for the table, or None if not found.
        """
        logging.info(f"Retrieving metadata for table: {table_name}")
        return self.metadata.get(table_name, None)


    def __init__(self):
        self.metadata = {}

    def add_metadata(self, table_name, description, source=None, additional_info=None):
        """
        Add metadata for a given table.

        Args:
            table_name (str): Name of the table to add metadata for.
            description (str): Description of the table.
            source (str, optional): Source of the table data.
            additional_info (str, optional): Any additional information related to the table.
        """
        self.metadata[table_name] = {
            "description": description,
            "source": source,
            "additional_info": additional_info
        }

    def get_metadata(self, table_name):
        return self.metadata.get(table_name, None)



class Notifier:
    """
    This class is responsible for sending notifications, such as emails.
    """

    def send_email(self, recipient, subject, message):
        """
        Simulate sending an email.
        
        :param recipient: The recipient of the email.
        :param subject: The subject of the email.
        :param message: The message body of the email.
        """
        logging.info(f"Sending email to {recipient} with subject: {subject}")
        # Simulated email sending
        print(f"Email sent to {recipient} with subject: {subject}\nMessage: {message}\n")
    
    def send_email(self, recipient, subject, message):
        # Simulating email sending
        print(f"Email sent to {recipient} with subject: {subject}\nMessage: {message}\n")
