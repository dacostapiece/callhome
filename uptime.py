import os
from datetime import datetime

def create_test_py(folder_path):
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Set the file path
        file_path = os.path.join(folder_path, 'test.py')

        # Open the file in write mode
        with open(file_path, 'a') as f:  # Use 'a' mode for append
            # Get the current system time
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Write some sample content to the file with current time
            f.write(f'# Current time: {current_time}\n')
        print(f"File '{file_path}' updated successfully.")
    except Exception as e:
        print("Error:", e)

# Call the function to update the file in a specific folder
folder_path = '/home/dacosta/Desktop'
create_test_py(folder_path)
