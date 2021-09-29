# Bluecoat_SiteReview
Get Domain/URL category by BlueCoat SiteReview with unlimited requests.


## Requirements:
-	You have to install pytesseract python library first using:	 ```pip install pytesseract```
-	Install pillow python library using: ```pip install pillow```
-	Download and Install "tesseract" using this link: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe 
-	Install "tesseract" inside the project directory, so the installation directory would look like, for example: ```C:\Users\<username>\Desktop\<script_folder_name>\pytesseract```


## Changes:
- I have decided to fork this project, to adjust the script and make it read a bulk of hashes from an input file, and output the not malicious (not yet identified by Bluecoat Sitereview) which you will need to block in your environment.
- Fixed some bugs in the way the script handles the captcha check and wrong domain checks.
- Fixed category name not parsed correctly.
- Added proxy support, if you are running this script behind proxy.


## Usage:
- Edit the script before you run it, add your proxy settings or comment the proxy block of code and also the requests line.
-	Put the Domains/URLs in a file called "iocs.txt", then put the text file In the same directory the script is running.
-	Run the following command: ```pyhton3 SiteReview.py```
-	Once the script has finished, you will see a list of Domains/URLs against their category available in your terminal window.
-	Also a txt file will be generated under the name "iocs_result.txt", which you will use to block Domains/URLs (not yet identified by Bluecoat).


## Bugs and Issues
Have a bug or an issue with the script? [Open a new issue](https://github.com/Mouhab-dev/Bluecoat_SiteReview/issues) here on GitHub.
