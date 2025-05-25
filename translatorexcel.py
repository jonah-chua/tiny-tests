import asyncio
import os
import pandas as pd
from playwright.async_api import Playwright, async_playwright, expect

async def cont()-> None:
        close_end=input(str("type 'c' to continue: "))
        if close_end=="c":
            print("ok, next/close")

async def closeall(context,browser)-> None:
    await context.close()
    await browser.close()

async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False,args=['--start-maximized'])
    context = await browser.new_context(no_viewport=True)
    page = await context.new_page()
    await page.goto("https://translate.google.com/?sl=zh-CN")
    await page.goto("https://translate.google.com/?sl=zh-CN&tl=en&op=translate")
    await page.get_by_label("Source text", exact=True).click()
    for col in df.columns:
        for idx in df.index:
            # If the cell is not empty
            if pd.notnull(df.loc[idx, col]) and df.loc[idx, col] != '':
                print(f'original:{df.loc[idx, col]}')
                await page.get_by_label("Source text", exact=True).fill(df.loc[idx, col])
                try:
                    print('i am here')    
                    if await page.locator("//span[contains(text(),'Try again')]").is_visible():
                        print("\n is visible")
                        await cont()
                        await page.locator("//span[contains(text(),'Try again')]").click()
                        print("\n clicked it\n")
                    df2.loc[idx, col]=await page.locator("//span[@class='ryNqvb']").inner_text()
                    #df2.loc[idx, col]=await page.get_by_role("region", name="Translation results").inner_text()
                except:
                    await cont()
                print(f'translated:{df2.loc[idx, col]}')
                await page.get_by_label("Source text", exact=True).fill('')
                try:
                    await page.wait_for_selector("//span[@class='ryNqvb']",state='hidden')
                except:
                    await cont()
            if idx==0:
                break


    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)
        df2.to_excel(output_path)
    print('printed to excel')

# Replace with your actual file path
file_loc = r"filepath.xlsx"  


df=pd.read_excel(file_loc, header=None)
df2=pd.DataFrame()
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'test1.xlsx')

asyncio.run(main())
