import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from urllib import response
import requests
import matplotlib.pyplot as plt
import pandas as pd
import datetime


root = Tk()
root.title('Currency Conversion')

root.geometry("600x600")
dict1={'US Dollar':'USD','European Euro': 'EUR', 'Japanese yen': 'JPY', 'Bulgarian lev': 'BGN', 'Czech koruna': 'CZK', 'Danish krone': 'DKK', 'British pound': 'GBP', 'Hungarian forint': 'HUF', 'Polish zloty': 'PLN', 'Romanian leu': 'RON', 'Swedish krona': 'SEK', 'Swiss franc': 'CHF', 'Icelandic króna': 'ISK', 'Norwegian krone': 'NOK', 'Croatian kuna': 'HRK', 'Turkish new lira': 'TRY', 'Australian dollar': 'AUD', 'Brazilian real': 'BRL', 'Canadian dollar': 'CAD', 'Chinese/Yuan renminbi': 'CNY', 'Hong Kong dollar': 'HKD', 'Indonesian rupiah': 'IDR', 'Indian rupee': 'INR', 'South Korean won': 'KRW', 'Mexican peso': 'MXN', 'Malaysian ringgit': 'MYR', 'New Zealand dollar': 'NZD', 'Philippine peso': 'PHP', 'Singapore dollar': 'SGD', 'Thai baht': 'THB', 'South African rand': 'ZAR'}
currencies=[i for i in dict1.keys()]
cr = CurrencyRates()
cc = CurrencyCodes()
# Create Tabs
my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=5)

# Create Two Frames
currency_frame = Frame(my_notebook, width=480, height=480)
conversion_frame = Frame(my_notebook, width=480, height=480)
trend_frame = Frame(my_notebook, width=480, height=480)

currency_frame.pack(fill="both", expand=1)
conversion_frame.pack(fill="both", expand=1)
trend_frame.pack(fill="both", expand=1)

# Add our Tabs
my_notebook.add(currency_frame, text="Currencies")
my_notebook.add(conversion_frame, text="Convert")
my_notebook.add(trend_frame, text="Conversion Trend")
# Disable 2nd tab
my_notebook.tab(1, state='disabled')
my_notebook.tab(2, state='disabled')

#######################
# CURRENCY STUFF
#######################
def lock():
	# print(,)

	home = home_selected.get()
	foreign=convert_select.get()
	if home==foreign:
		messagebox.showwarning("WARNING!", "Home currency and Foreign Currency are same")	
	else:
		print("Cool")
		# Disable entry boxes
		home_entry.config(state="disabled")
		conversion_entry.config(state="disabled")
		# rate_entry.config(state="disabled")
		# Enable tab
		my_notebook.tab(1, state='normal')
		my_notebook.tab(2, state='normal')

		plot_button = Button(master=trend_frame,
							 command=plot1(1, dict1[home], dict1[foreign], 365),
							 height=2,
							 width=10,
							 text="Plot")
		#rate_entry.delete(0,tkinter.END)
		#rate_entry.insert(0,str(cr.get_rate(dict1[home],dict1[foreign])))
		# Change Tab Field
		amount_label.config(text=f'Amount of {home} To Convert To {foreign}')
		converted_label.config(text=f'Equals This Many {foreign}')
		convert_button.config(text=f'Convert From {home}')
		rate_entry.config(state="normal")
		rate_entry.delete(0, END)
		conv_rate=round(cr.get_rate(dict1[home], dict1[foreign]),3)

		rate_entry.insert(0, conv_rate)
		rate_entry.config(state="disabled")
def unlock():
	# Enable entry boxes
	home_entry.config(state="normal")
	conversion_entry.config(state="normal")

	# rate_entry.config(state="normal")
	# Disable Tab

	my_notebook.tab(1, state='disabled')
	my_notebook.tab(2, state='disabled')
	#clear plot
	for widgets in trend_frame.winfo_children():
		widgets.destroy()
	#clear amount in convert
	clear()




home = LabelFrame(currency_frame, text="Your Home Currency")
home.pack(pady=20)


# Home currency entry box
# home_entry = Entry(home, font=("Helvetica", 24))
# home_entry.pack(pady=10, padx=10)
home_selected = StringVar()
 # default value

home_selected.set(currencies[0])
home_entry = OptionMenu(home,home_selected, *currencies)
home_entry.pack(pady=10, padx=10)
# Conversion Currency Frame
conversion = LabelFrame(currency_frame, text="Conversion Currency")
conversion.pack(pady=20)

# convert to label
conversion_label = Label(conversion, text="Currency To Convert To...")
conversion_label.pack(pady=10)

# Convert To Entry
convert_select = StringVar()
 # default value

convert_select.set(currencies[0])
conversion_entry = OptionMenu(conversion,convert_select, *currencies)
conversion_entry.pack(pady=10, padx=10)



# Button Frame
button_frame = Frame(currency_frame)
button_frame.pack(pady=20)

# Create Buttons
lock_button = Button(button_frame, text="Lock", command=lock)
lock_button.grid(row=0, column=0, padx=10)

unlock_button = Button(button_frame, text="Unlock", command=unlock)
unlock_button.grid(row=0, column=1, padx=10)


#######################
# CONVERSION STUFF
#######################
def convert():
	val=float(amount_entry.get())
	home=home_selected.get()
	foreign=convert_select.get()
	# Clear Converted Entry Box
	converted_entry.delete(0, END)

	# Convert
	conversion = val * cr.get_rate(dict1[home],dict1[foreign])
	# Convert to two decimals
	conversion = round(conversion,3)
	# Add commas
	conversion = '{:,}'.format(conversion)
	
	symbol = cc.get_symbol(dict1[foreign])
	# Upodate entry box
	converted_entry.insert(0, f'{symbol} {conversion}')	
def clear():
	amount_entry.delete(0, END)
	converted_entry.delete(0, END)

amount_label = LabelFrame(conversion_frame, text="Amount To Convert")
amount_label.pack(pady=20)

# Entry Box For Amount
amount_entry = Entry(amount_label, font=("Helvetica", 24))
amount_entry.pack(pady=10, padx=10)

# Convert Button
convert_button = Button(amount_label, text="Convert", command=convert)
convert_button.pack(pady=20)

# Equals Frame
rate_label1 = LabelFrame(conversion_frame, text="Rate")
rate_label1.pack(pady=20)

# rate label
rate_label = Label(rate_label1, text="Current Conversion Rate...")
rate_label.pack(pady=10)

# # Rate To Entry
rate_entry = Entry(rate_label1, font=("Helvetica", 24))
rate_entry.delete(0,END)
#conv_rate=cr.get_rate(dict1[home],dict1[foreign])
#print(conv_rate)

#rate_entry.insert(0,cr.get_rate(dict1[homecur],dict1[foreigncur]))
rate_entry.pack(pady=10, padx=10)
rate_entry.config(state="disabled")



# Equals Frame
converted_label = LabelFrame(conversion_frame, text="Converted Currency")
converted_label.pack(pady=20)

# Converted entry
converted_entry = Entry(converted_label, font=("Helvetica", 24), bd=0, bg="systembuttonface")
converted_entry.pack(pady=10, padx=10)

# Clear Button
clear_button = Button(conversion_frame, text="Clear", command=clear)
clear_button.pack(pady=20)

# Fake Label for spacing
spacer = Label(conversion_frame, text="", width=68)
spacer.pack()

def plot1(amount,currency,converted_currency,amount_of_days):
	# the figure that will contain the plot

	fig = Figure(figsize=(5, 5), dpi=100)

	today_date = datetime.datetime.now()
	date_1year = (today_date - datetime.timedelta(days=1 * amount_of_days))

	url = f'https://api.exchangerate.host/timeseries'
	payload = {'base': currency, 'amount': amount, 'start_date': date_1year.date(), 'end_date': today_date.date()}
	response = requests.get(url, params=payload)
	data = response.json()

	currency_history = {}
	rate_history_array = []

	for item in data['rates']:
		current_date = item
		currency_rate = data['rates'][item][converted_currency]

		currency_history[current_date] = [currency_rate]
		rate_history_array.append(currency_rate)

	pd_data = pd.DataFrame(currency_history).transpose()
	pd_data.columns = ['Rate']
	pd.set_option('display.max_rows', None)
	print(pd_data)

	plt = fig.add_subplot(111)
	plt.plot(rate_history_array)
	plt.set_ylabel(f'{amount} {currency} to {converted_currency}')
	plt.set_xlabel('Days')
	plt.set_title(f'Current rate for {amount} {currency} to {converted_currency} is {rate_history_array[-1]}')
	# plt.show()

	# creating the Tkinter canvas
	# containing the Matplotlib figure

	canvas = FigureCanvasTkAgg(fig,
							   master=trend_frame)
	canvas.draw()

	# placing the canvas on the Tkinter window
	canvas.get_tk_widget().pack()

	# creating the Matplotlib toolbar
	toolbar = NavigationToolbar2Tk(canvas,
								   trend_frame)
	toolbar.update()

	# placing the toolbar on the Tkinter window
	canvas.get_tk_widget().pack()




root.mainloop()


