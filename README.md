# GorillaFTP
## About
GorillaFTP is a small, modern, free and open-source FTP client. It's made as an alternative to FileZilla and other FTP clients.
But it's still not that powerful to compete with other FTP clients. Only an alpha version.

## Building the program from source
1. Install [Python](https://python.org)
2. Clone the sources with GitHub Desktop or this command:
```git
git clone https://github.com/Halcyon-Software/GorillaFTP.git
```
3. Open the command prompt in the folder that you copied GorillaFTP repository to
4. Install `pyinstaller` with this command:
```pip
pip install pyinstaller
```
5. Run this command:
```pip
pyinstaller --onefile main.pyw
```
6. A folder called `dist` should appear, there is the EXE file of GorillaFTP inside of it.
7. Done!
