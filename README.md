![Alt text](https://raw.github.com/lettier/cryptohoppershouter/master/screenshot.jpg)

# CryptoHopper and CryptoShouter

CryptoHopper takes a specified out folder/directory, encrypts the files contained within (with a .comp extension), and then moves these files to a specified encrypted folder. Files without the extension .comp and/or files older than 30 days are removed from the specified out folder. Needs (Python-GNUPG)[http://code.google.com/p/python-gnupg/].  

CryptoShouter takes a specified encrypted folder and then emails the files with a .comp extension contained within the encrypted folder to specified email addresses. After emailing, it moves the files from the encrypted folder to a specified trash folder. Files older than 30 days in the trash folder are removed.  

Both CryptoHopper and CryptoShouter can be run as cron jobs.

Files and directories located at:  

- ./source/out
- ./source/encrypted/
- ./source/trash

are provided for testing/convenience. Feel free to specify your own directories on the command line.

./test_setup contains a bash script that initializes the aforementioned directories with test files&mdash;some of which have had their mtime modified such that they are older than 30 days.  

_(C) 2014 David Lettier._  
http://www.lettier.com/