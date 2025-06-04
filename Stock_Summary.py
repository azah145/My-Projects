import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path="API.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stock_scraper(ticker):
	print(f"\nFetching stock information for {ticker}...")
	url = f"https://finance.yahoo.com/quote/{ticker}/analysis"
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	data = {}

	try:
		tables = soup.find_all('table')
		for table in tables:
			if 'Earnings Estimate' in table.text:
				eps_rows = table.find_all('tr')
				for row in eps_rows:
					cells = row.find_all('td')
					if cells and 'Avg. Estimate' in cells[0].text:
						data['EPS Estimates'] = [cell.text for cell in cells[1:]]
						break
				break
	except Exception as e:
		print(f" Error fetching EPS data: {e}")
		data['EPS Estimates'] = 'Unavailable'

	return data

def build_prompt(ticker, stock_data):
	eps = stock_data.get("EPS Estimates", "Unavailable")
	if eps == "Unavailable":
		return f"Unable to retrieve EPS estimates for {ticker}."
	else:
		return (
			f"The average EPS estimates for {ticker} over upcoming periods are: "
			f"{', '.join(eps)}. Please summarize the earnings trend and explain what it means "
			f"for an investor in simple terms."
		)

def get_ai_summary(prompt):
	try:
		response = client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are a financial assistant who summarizes EPS trends."},
				{"role": "user", "content": prompt}
			],
			max_tokens=200,
			temperature=0.5
		)
		return response.choices[0].message.content.strip()
	except Exception as e:
		return f" OpenAI request failed: {e}"

def save_to_file(ticker, raw_data, summary):
	filename = f"{ticker}_summary.txt"
	with open(filename, "w", encoding="utf-8") as f:
		f.write(f"Ticker: {ticker}\n\n")
		f.write("=== Raw EPS Estimates ===\n")
		f.write(", ".join(raw_data.get("EPS Estimates", [])) + "\n\n")
		f.write("=== AI Summary ===\n")
		f.write(summary)
	print(f"\n Results saved to {filename}")

while True:
	response = input("Would you like to research a stock? (yes/no): ").strip().lower()

	if response == 'yes':
		ticker = input("Please enter the stock ticker symbol: ").strip().upper()
		print(f"\n You entered: {ticker}")

		stock_data = stock_scraper(ticker)
		prompt = build_prompt(ticker, stock_data)
		ai_summary = get_ai_summary(prompt)

		print("\n AI Summary:\n")
		print(ai_summary)

		save_to_file(ticker, stock_data, ai_summary)
		break

	elif response == 'no':
		print("Thank you for using our resources.")
		break

	else:
		print(" Invalid response. Please type 'yes' or 'no'.")
	
		

	