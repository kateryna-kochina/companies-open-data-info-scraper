import csv


class CsvManager:
    @staticmethod
    def write_to_csv(header, scraped_data, output_path):
        '''
        Write data to a CSV file.

        Args:
            header (list): List of header fields.
            scraped_data (list): List of lists containing data to be written.
            output_path (str): Path to the output CSV file.
        '''
        try:
            # Append data to the CSV file
            with open(output_path, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                # Write the header if the file is empty
                if csv_file.tell() == 0:  # Check if the file is empty
                    csv_writer.writerow(header)

                # Write the data
                csv_writer.writerows(scraped_data)

        except Exception as e:
            print(f'Error writing to CSV: {e}')

    @staticmethod
    def read_csv(file_path):
        '''
        Read data from a CSV file.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            list: List of lists containing the CSV data.
        '''
        data = []
        try:
            with open(file_path, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # Skip header row
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f'Error reading CSV: {e}')

        return data
