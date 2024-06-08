import os

def create_test_py(folder_path):
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Set the file path
        file_path = os.path.join(folder_path, 'test.py')

        # Open the file in write mode
        with open(file_path, 'w') as f:
            # Write some sample content to the file
            f.write('print("Hello, world!")\n')
            f.write('print("This is a test script.")\n')
            f.write('print("You can modify it as needed.")\n')
        print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print("Error:", e)

# Call the function to create the file in a specific folder
folder_path = '/home/dacosta/Desktop'
create_test_py(folder_path)
