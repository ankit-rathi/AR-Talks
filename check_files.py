    def check_files(self, available_files_json):
        """
        Reads from Kafka topic, checks if file_names in available_files_json exist in the Kafka messages.
        
        Args:
        - available_files_json (dict): A dictionary that contains available file names in the format:
                                       {"file_names": "file1.zip,file2.zip,file3.zip"}
                                       
        Returns:
        - "PASS" if all file_names are found in Kafka messages.
        - "FAIL" if any file_name is missing.
        """
        # Extract and split available file names
        available_files = set(available_files_json.get('file_names', "").split(','))
        found_files = set()
        
        # Connect to Kafka
        consumer = self._connect_kafka()
        
        # Poll the Kafka topic for messages
        for message in consumer:
            # Extract the file path from the Kafka message's "key"
            file_path = message.value.get("key", "")
            
            # Extract the file name from the file path (e.g., file1.zip)
            file_name = os.path.basename(file_path)
            
            # Add the file name to found_files if it's in available_files
            if file_name in available_files:
                found_files.add(file_name)
            
            # Check if all files have been found
            if found_files == available_files:
                return "PASS"
        
        # If the loop ends without finding all files, return "FAIL"
        return "FAIL"
