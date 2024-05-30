from bs4 import BeautifulSoup
import asyncio
from pyppdf.patch_pyppeteer import patch_pyppeteer
from pyppeteer import launch
import tkinter as tk
from itertools import zip_longest
import webbrowser

# URLs to scrape
urls = ['https://careerviet.vn/viec-lam/Odoo-tai-ho-chi-minh-kl8-vi.html'
   ,'https://www.topcv.vn/tim-viec-lam-odoo-tai-ho-chi-minh-kl2']

# Define job_titles_page1 and job_titles_page2 as global variables
global job_titles_page1
global job_titles_page2 

desired_titles = ['Odoo', 'BA', 'Business Analyst', 'FC', 'Functional Consultant','Triển']
undesired_titles = []

async def get_html(url):
    patch_pyppeteer()
    browser = await launch(executablePath='D:\\Scrap Recruiment\\Win_x64_869685_chrome-win\\chrome-win\\chrome.exe')  # replace with the actual path to your chrome.exe
    page = await browser.newPage()
    for _ in range(3):  # retry 3 times
        try:
            await page.goto(url)
            break
        except ConnectionResetError:
            print(f"Connection reset by peer, retrying...")
    else:
        print(f"Failed to access {url} after 3 attempts")
        return None
    content = await page.content()

    await browser.close()
    return content



for url in urls:
    # Get the HTML content of the page
    loop = asyncio.get_event_loop()
    html = loop.run_until_complete(get_html(url))
    if html is None:
        continue

    # Parse the source with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

  

    # Check the URL to determine the tag and class to use
    if 'https://careerviet.vn/viec-lam/Odoo-tai-ho-chi-minh-kl8-vi.html' in url:  # page1
        tag = 'a'
        class_x = 'job_link'
        job_titles_page1 = [job.text.strip() for job in soup.find_all(tag, class_x) if any(title in job.text for title in desired_titles) and not any(title in job.text for title in undesired_titles)]
    elif 'https://www.topcv.vn/tim-viec-lam-odoo-tai-ho-chi-minh-kl2' in url:  # page2
        tag = 'h3'
        class_x = 'title'
        job_titles_page2 = [job.text.strip() for job in soup.find_all(tag, class_x) if any(title in job.text for title in desired_titles) and not any(title in job.text for title in undesired_titles)]
    else:
        tag = 'NA'
        class_x = 'NA'
   
def open_webpage(url):
    webbrowser.open(url)

def show_job_titles():
    window = tk.Toplevel()

    # Create labels for the page names
    label1 = tk.Label(window, text="careerviet")
    label1.grid(row=0, column=0)
    label1.bind("<Button-1>", lambda e, url='https://careerviet.vn/viec-lam/Odoo-tai-ho-chi-minh-kl8-vi.html': open_webpage(url))

    label2 = tk.Label(window, text="topcv")
    label2.grid(row=0, column=1)
    label2.bind("<Button-1>", lambda e, url='https://www.topcv.vn/tim-viec-lam-odoo-tai-ho-chi-minh-kl2': open_webpage(url))

    # Display the job titles
    for i, (job_title_page1, job_title_page2) in enumerate(zip_longest(job_titles_page1, job_titles_page2), start=1):  # start=1 to leave the first row for the page names
        if job_title_page1 is not None:
            label = tk.Label(window, text=job_title_page1)
            label.grid(row=i, column=0)  # Display job titles from page1 in column 0
            label.bind("<Button-1>", lambda e, url='https://careerviet.vn/viec-lam/Odoo-tai-ho-chi-minh-kl8-vi.html': open_webpage(url))

        if job_title_page2 is not None:
            label = tk.Label(window, text=job_title_page2)
            label.grid(row=i, column=1)  # Display job titles from page2 in column 1
            label.bind("<Button-1>", lambda e, url='https://www.topcv.vn/tim-viec-lam-odoo-tai-ho-chi-minh-kl2': open_webpage(url))

  

root = tk.Tk()
button = tk.Button(root, text="Show job_titles", command=show_job_titles)
button.pack()
root.mainloop()