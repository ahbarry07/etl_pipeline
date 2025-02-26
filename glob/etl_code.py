import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

log_file = "log_file.txt" 
target_file = "data/transformed_data.csv" 


def extract_from_csv(file_to_process):
    '''This function extract data from csv file'''

    df = pd.read_csv(file_to_process)
    return df


def extract_from_json(file_to_process):
    '''This function extract data from json file'''

    df = pd.read_json(file_to_process, lines=True)
    return df


def extract_from_xml(file_to_process):
    '''This function extract data from xml file'''

    df = pd.DataFrame(columns=['name', 'height', 'weight'])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find('name').text
        height = float(person.find('height').text)
        weight = float(person.find('weight').text)
        
        df = pd.concat([df, pd.DataFrame([{'name': name, 'height': height, 'weight': weight}])], ignore_index=True)  
    return df


def extract():
    '''This function extracts data from CSV, JSON, and XML files. 
    It consolidates the extracted information into a single pandas DataFrame with the columns 
    'name', 'height', and 'weight'. The function returns the DataFrame for further processing.'''

    extracted_data = pd.DataFrame(columns=['name', 'height', 'weight'])

    # process all csv files
    for csvfile in glob.glob('data/*.csv'):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True)

    # process all json files
    for jsonfile in glob.glob('data/*.json'):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True)

    # process all xml files
    for xmlfile in glob.glob('data/*.xml'):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True)

    return extracted_data


def transform(data):
    '''Convert inches to meters and round off to two decimals 
    1 inch is 0.0254 meters '''

    data['height'] = round(data.height * 0.0254, 2)

    '''Convert pounds to kilograms and round off to two decimals 
    1 pound is 0.45359237 kilograms '''

    data['weight'] = round(data.weight * 0.45359237,2) 
    
    return data


def load_data(target_file, transformed_data):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    transformed_data.to_csv(target_file)


def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(log_file, 'a') as f:
        f.write(timestamp + ',' + message + '\n')


if __name__== '__main__':
    # Log the initialization of the ETL process 
    log_progress("ETL Job Started") 
    
    # Log the beginning of the Extraction process 
    log_progress("Extract phase Started") 
    extracted_data = extract() 
    
    # Log the completion of the Extraction process 
    log_progress("Extract phase Ended") 
    
    # Log the beginning of the Transformation process 
    log_progress("Transform phase Started") 
    transformed_data = transform(extracted_data) 
    print("Transformed Data") 
    print(transformed_data) 
    
    # Log the completion of the Transformation process 
    log_progress("Transform phase Ended") 
    
    # Log the beginning of the Loading process 
    log_progress("Load phase Started") 
    load_data(target_file,transformed_data) 
    
    # Log the completion of the Loading process 
    log_progress("Load phase Ended") 
    
    # Log the completion of the ETL process 
    log_progress("ETL Job Ended") 