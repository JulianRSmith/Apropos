----------------------------------------------------------------------------------------
---------------------------------------- README ----------------------------------------
----------------------------------------------------------------------------------------


----------------------------------------------------------------------------------------
Prerequisites
----------------------------------------------------------------------------------------
- Python 3.0 or higher (https://goo.gl/xpldVP)
- BeautifulSoup4 module (https://goo.gl/2OXs3u)
- PyMySQL module (https://goo.gl/fl6hJt)
- A web browser of your choice (latest version of Google Chrome is recommended)
- A constant internet connection
- A text editor or IDE of your choice

----------------------------------------------------------------------------------------
Running & Operating The Web Crawler & Indexer
----------------------------------------------------------------------------------------
To run the program:
1. Open the command prompt. On Windows: Start -> Run -> type “cmd” in the
input box. On macOS/OS X: Finder -> Applications -> Utilities -> Terminal
2. Navigate to the location of the main.py file on the USB. In Windows and macOS /
OSX: cd [USB LOCATION]:\Apropos\Web Crawler and Indexer
3. Run the program using the following command: “main.py” - If a problem occurs,
see https://docs.python.org/3/faq/windows.html
To operate the program:
1. First type in the website you want to index, for example “https://
www.example.com"
2. The program will check if the website you inputed is the correct website to index,
press “y” if it is, or “n” if it isn’t, and “enter”.
3. It will then ask you how many pages to index, if you don't want a limit to the
number of pages, simply type “0” and “enter”.
4. The program will then ask you if you want to enter advanced options, if you do
“y” to do so, or “n” if not, and “enter”.
5. If you chose to enter advanced options, you would be given the option to enter
“Definition and Code settings”, type “y” to do so, or “n” if not, and “enter”. Here
you can input the class name of the div that contain the definition and the code.
You will also be presented with options such as the title and description class
names of the divs that contain them. Also in advanced options you can add
keywords that will be applicable to the whole website. For example, inputing “test
, this is , a test” will apply “test”, “this is”, and “a test” as the keywords to the
website. There is also the option to only index a page if it contains certain words,
which is applied in the same way the keywords are applied. Lastly in advanced
options you can turn indexing to the database off by typing “y” to do so, or “n” if
not, and “enter”. Turning the index off is recommend for testing as results of
which will appear on the front end website.
6. The system will then begin to index every page on the website until the index limit
is reached or there are no more pages to visit.

----------------------------------------------------------------------------------------
Running The Website
----------------------------------------------------------------------------------------
To run the website:
1. On a browser of your choice, visit www.apropos.tech . To see the source code,
open any file in the “Website” folder of the USB using a text editor or IDE of your
choice.

----------------------------------------------------------------------------------------
Search Queries That Return Results
----------------------------------------------------------------------------------------
- "brighton"
- "html"
- "visit"
- "java"
- "hockey"
- "django"
- "character sets"
- "empty" - will return no results 