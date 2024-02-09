import requests
import csv
import re
import os
from datetime import datetime

# Function to extract data from JSON
def extract_data(json_data, download_folder):
    extracted_data = []
    unique_number = 1

    def get_party_number(party_name):
        party_dict = {
            "Partai Kebangkitan": 1,
            "Partai Gerakan Indonesia Raya": 2,
            "Partai Demokrasi Indonesia Perjuangan": 3,
            "Partai Golongan Karya": 4,
            "Partai NasDem": 5,
            "Partai Buruh": 6,
            "Partai Gelombang Rakyat Indonesia": 7,
            "PARTAI KEADILAN SEJAHTERA": 8,
            "Partai Kebangkitan Nusantara": 9,
            "Partai Hati Nurani Rakyat": 10,
            "Partai Garda Republik Indonesia": 11,
            "Partai Amanat Nasional": 12,
            "Partai Bulan Bintang": 13,
            "Partai Demokrat": 14,
            "Partai Solidaritas Indonesia": 15,
            "PERINDO": 16,
            "Partai Persatuan Pembangunan": 17,
            "Partai Ummat": 18

        }
        return party_dict.get(party_name, "0")

    for item in json_data['data']:
        party_name_match = re.search(r'>([^<]+)', item[0])
        party_name = party_name_match.group(1).strip() if party_name_match else ""

        candidate_number_match = re.search(r'<b><font size="3">(\d+)</font></b>', item[2])
        nourut_caleg = candidate_number_match.group(1).strip() if candidate_number_match else ""

        # Extract image link
        image_link_match = re.search(r'src="([^"]+)"', item[3])
        image_link = image_link_match.group(1).strip() if image_link_match else ""

        namacaleg = item[4].strip()
      

        # Download and save the image locally with a unique number and candidate details
        candidate_name_no_space = namacaleg.replace(" ", "")
        party_name_no_space = party_name.replace(" ", "")
        potocaleg = os.path.join(download_folder, f"{party_name_no_space}_{nourut_caleg}_{candidate_name_no_space}_{unique_number}.jpeg")
        
        try:
            download_image(image_link, potocaleg)
            print(f"Image {unique_number} downloaded successfully to {potocaleg}")
        except requests.exceptions.Timeout:
            print(f"Image {unique_number} download timed out. Moving on to the next image.")

        idpartai =  get_party_number(party_name)
        idkategori = 1
        idkabupaten = 11.00
        iddapil = 17




        extracted_data.append([idkategori, idpartai, idkabupaten, iddapil,nourut_caleg,namacaleg,potocaleg])
        unique_number += 1

    return extracted_data

# Function to download an image and save it locally
def download_image(image_url, local_filename):
    response = requests.get(image_url, stream=True, timeout=30)
    with open(local_filename, 'wb') as image_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                image_file.write(chunk)

# Function to fetch data from URL and convert it to JSON
def fetch_json_data(url):
    response = requests.get(url)
    json_data = response.json()
    return json_data

# Create a folder to store downloaded images
download_folder = "/opt/python/downloaded_images_halmahera5"
os.makedirs(download_folder, exist_ok=True)

# URL for fetching JSON data
# url = "https://infopemilu.kpu.go.id/Pemilu/Dct_dprd/Dct_dprdkabko?kode_dapil=730402&_=1707299235972"
# url = "https://infopemilu.kpu.go.id/Pemilu/Dct_dprprov/Dct_dprprov?kode_dapil=120001&_=1707216263040"
url = "https://infopemilu.kpu.go.id/Pemilu/Dct_dprd/Dct_dprdkabko?kode_dapil=820405&_=1707474868553"


# Fetch JSON data from the URL
json_data = fetch_json_data(url)

# Extract data from JSON and download images
extracted_data = extract_data(json_data, download_folder)

# Write data to CSV
csv_filename = "extracted_data_halmahera5.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write header
    csv_writer.writerow(['idkategori', 'idpartai', 'idkabupaten', 'iddapil', 'nourut_caleg', 'namacaleg','potocaleg'])
    
    # Write rows
    csv_writer.writerows(extracted_data)

print(f"Data has been extracted, saved to {csv_filename}, and images have been downloaded to {download_folder}.")
