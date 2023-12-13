#-------------------------------------------------------------------------------
# Name:         create_zip.py
# Purpose:      This Python script takes an input folder and creates a zip file and stores in the output folder. 
# Author:       Kiran Chandrashekhar
# Created:      18-Dec-2022
#-------------------------------------------------------------------------------

import os
from random import randint
import zipfile
import shutil
import argparse
import sys

class CreateZip:
    def __init__(self):
        pass

    def get_all_files(self, directory:str)->list:
        """
        Get all the files from the directory
        """
        complete_file_list = []
        for dirname, subdirs, files in os.walk(directory):                
            file_list = [os.path.join(dirname, file) for file in files]
            complete_file_list.extend(file_list)
      
        return complete_file_list

    #-------------------------------------------------#
    #   Create Zip File from the folder - v1          #
    #-------------------------------------------------#

    def create_zip_file(self, directory:str)->str:
        """
        Create a zip file from the list of all the file from the 
        specified directory
        """
        file_list = self.get_all_files(directory)
        zip_file = f"{os.getcwd()}/output/{randint(100_000,999_999)}.zip"
        
        with zipfile.ZipFile(zip_file, "w") as zf:
            for file in file_list:                
                relative_path = os.path.relpath(file, directory)     
                zf.write(file, relative_path)
        return zip_file


    #-------------------------------------------------#
    #   Create Zip File from the folder - v2          #
    #-------------------------------------------------#

    def create_zip_file_v2(self, directory:str,filename:str)->str:
        """
        Create a zip file from the list of all the file from the 
        specified directory
        """
        if os.path.exists(f'{os.getcwd()}/output/')==False:
            os.mkdir(f'{os.getcwd()}/output/')
        zip_file = f"{os.getcwd()}/output/{filename}"
        zip_path = shutil.make_archive(zip_file, 'zip', directory)
        return zip_path

    #-------------------------------------------------#
    #  Unzip the file                                 #
    #-------------------------------------------------#
    def unzip_file(self, zip_file:str)->str:
        """
        Unzip the file and save the extracted files in the output folders
        """
        output_folder = f"{os.getcwd()}/output/{randint(100_000,999_999)}"
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(output_folder)  
        return output_folder

def main(filename=None):

    obj = CreateZip()
    directory = f"{os.getcwd()}/build/"

    if sys.platform == 'win32':
        directory = f"{os.getcwd()}/dist/"
    elif sys.platform == 'darwin': 
        pass
    else:
        directory = f"{os.getcwd()}/build/"


    zip_file_path = obj.create_zip_file_v2(directory,filename)
    # output_folder = obj.unzip_file(zip_file_path)
    # print(output_folder)
   

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help="Specify the zipfilename")
    args = parser.parse_args()
    main(args.filename)
    print("Done")