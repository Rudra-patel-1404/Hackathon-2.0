import webbrowser
import os

def open_browser():
    # Get the absolute path of the HTML file
    html_path = os.path.abspath('html_pages/index.html')
    
    # Open the file in the default browser
    webbrowser.open('file://' + html_path)
    
    print("Opening Resource Hub in your browser...")

if __name__ == "__main__":
    open_browser() 