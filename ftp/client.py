from ftplib import FTP


class FTPClient:
    def __init__(self):
        self.ftp = None
        self.current_path = "/"

    def connect(self, host, port, username, password):
        self.ftp = FTP()
        self.ftp.connect(host, int(port))
        self.ftp.login(username, password)
        self.current_path = "/"

    def list_dir(self):
        items = []

        try:
            self.ftp.cwd(self.current_path)
            raw = []

            self.ftp.retrlines("LIST", raw.append)

            for line in raw:
                parts = line.split()
                name = parts[-1]

                is_dir = line.startswith("d")

                items.append({
                    "name": name,
                    "is_dir": is_dir
                })

        except Exception:
            pass

        return items

    def change_dir(self, folder):
        if folder == "..":
            if self.current_path != "/":
                self.current_path = "/".join(self.current_path.rstrip("/").split("/")[:-1])
                if self.current_path == "":
                    self.current_path = "/"
        else:
            if self.current_path == "/":
                self.current_path += folder
            else:
                self.current_path += "/" + folder

        self.ftp.cwd(self.current_path)

    def upload(self, file_path):
        with open(file_path, "rb") as f:
            name = file_path.split("/")[-1].split("\\")[-1]
            self.ftp.storbinary(f"STOR {name}", f)

    def download(self, remote_name, local_path):
        with open(local_path, "wb") as f:
            self.ftp.retrbinary(f"RETR {remote_name}", f.write)

    def delete(self, name):
        try:
            self.ftp.delete(name)
        except:
            self.ftp.rmd(name)

    def rename(self, old, new):
        self.ftp.rename(old, new)

    def mkdir(self, name):
        self.ftp.mkd(name)

    def get_path(self):
        return self.current_path