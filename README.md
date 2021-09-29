# Bluecoat_SiteReview
Get Domain/URL category by BlueCoat SiteReview with unlimited requests.


## Requirements:
-	You have to install pytesseract python library first using:	 ```pip install pytesseract```
-	Install pillow python library using: ```pip install pillow```
-	Download and Install "tesseract" using this link: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe 
-	Install "tesseract" inside the project directory, so the installation directory would look like ```C:\Users\\<$username>\Desktop\\<$script_folder_name>\pytesseract```


## Changes:
- I have decided to fork this project, to adjust the script and make it read a bulk of hashes from an input file, and output the not malicious (not yet identified by Bluecoat Sitereview) which you will need to block in your environment.
- Fixed some bugs in the way the script handles the captcha check and wrong domain checks.
- Fixed category name not parsed correctly.


## Usage:
-	Download and change the attached file’s extension to .py
-	Put the Domains/URLs in a file called "iocs.txt", then put the text file In the same directory the script is running.
-	Run the following command: pyhton3 bluecoat-checker.py
-	Once the script has finished, you will see a list of Domains/URLs against their category available in your terminal window.
-	Also a txt file will be generated under the name "iocs_result.txt", which you will use to block Domains/URLs (not yet identified by Bluecoat).


## Bugs and Issues
Have a bug or an issue with the website? [Open a new issue](https://github.com/Mouhab-dev/Bluecoat_SiteReview/issues) here on GitHub.
