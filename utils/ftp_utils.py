import ftplib
import logging
from ftplib import FTP
from datetime import datetime


def upload_file(local_file_path, remote_file_path, hostname, username, password):
    try:
        ftp = FTP(hostname)
        ftp.login(username, password)

        with open(local_file_path, 'rb') as file:
            ftp.storbinary('STOR ' + remote_file_path, file)

        logging.info(f"File '{local_file_path}' uploaded successfully to '{remote_file_path}' on the FTP server.")
        ftp.quit()
    except ftplib.all_errors as e:
        logging.info(f"FTP error occurred: {str(e)}")

def update_sitemap(file_name, ftp_host, ftp_username, ftp_password, path):
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_username, passwd=ftp_password)
    files = ftp.nlst()
    existing_sitemap = "sitemap.xml" in files
    file_index = files.index(file_name)
    file_name = file_name.replace(' ', '%20')
    sitemap_path = path + "sitemap.xml"
    if existing_sitemap:
        ftp.retrbinary("RETR sitemap.xml", open(sitemap_path, "wb").write)
        with open(sitemap_path, "r+") as f:
            lines = f.readlines()
            f.seek(0)

            for line in lines:
                if "<urlset" in line:
                    f.write(line)
                    f.write('\t<url>\n')
                    f.write(f'\t\t<loc>https://oniichan.in/web-stories/{file_name}</loc>\n')
                    timestamp = ftp.voidcmd(f"MDTM {files[file_index]}")[4:].strip()
                    last_modified = datetime.strptime(timestamp, "%Y%m%d%H%M%S").isoformat()
                    last_modified = last_modified + "+00:00"
                    f.write(f'\t\t<lastmod>{last_modified}</lastmod>\n')
                    f.write('\t\t<priority>0.80</priority>\n')
                    f.write('\t</url>\n')
                else:
                    f.write(line)

            f.truncate()

        ftp.storlines("STOR sitemap.xml", open(sitemap_path, "rb"))
        logging.info("Sitemap Updated Successfully")
    else:
        logging.info("sitemap not found")

    ftp.quit()
