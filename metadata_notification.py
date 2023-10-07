class MetadataManager:
    def __init__(self):
        self.metadata = {}

    def add_metadata(self, table_name, description, source=None, additional_info=None):
        self.metadata[table_name] = {
            "description": description,
            "source": source,
            "additional_info": additional_info
        }

    def get_metadata(self, table_name):
        return self.metadata.get(table_name, None)


class Notifier:
    def send_email(self, recipient, subject, message):
        # Simulating email sending
        print(f"Email sent to {recipient} with subject: {subject}\nMessage: {message}\n")
