import os

def remove_zone_identifier_files(directory):
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(":Zone.Identifier"):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Removed {file_path}")
        print("Finished removing Zone.Identifier files.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


current_directory = os.getcwd()
remove_zone_identifier_files(current_directory)

# git config --global user.name "mujtaba"
# git config --global user.email "mujtabajafri3@gmail.com"
# git commit -m "first commit"