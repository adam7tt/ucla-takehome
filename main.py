import requests
import csv
from utils import get_change, prime_factorization, back_to_int
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main():
    response = requests.get("https://datausa.io/api/data?drilldowns=State&measures=Population").json()['data']
    seen = {}

    state_data = []

    for row in reversed(response):
        #Utilize Slug State because the slug will/should be a unique value and store it in a dictionary for ease of access
        if row['Slug State'] in seen:
            #Iterate through the array of dictionaries containing the state population data in order to access previously allocated states
            state_index = next((index for (index, d) in enumerate(state_data) if d["State"] == row['State']), None)
            #Because the population data is being written as a string of format 2013 (N%) we need to convert it back into a number to calculate growth/decline percent from the previous year
            #We could save this step by saving a copy as an number and one as a formatted string and only writing the string
            last_year = float(state_data[state_index][row['ID Year'] - 1].split('(')[0])
            this_year = row['Population']
            change = get_change(this_year, last_year)
            state_data[state_index][row['ID Year']] = str(row['Population']) + str(f"({change:.2f}%)")
        else:
            #if not seen allocate to dict with an arbitrary value and odd first instance to state data array
            seen[row['Slug State']] = 1
            state_data.append({"State" : row['State'], row['ID Year'] : str(row['Population'])})

    #Open a file in the directory called data_file.csv and allocate the keys of the first row of data to be it's headers. Each item in the array is an instance of the same object so the index used here is arbitrary
    data_file = open('data_file.csv', 'w')
    output = csv.writer(data_file)
    
    header_row = list(state_data[0].keys())
    header_row.append(str(header_row[-1]) + " Factorization")
    output.writerow(header_row)

    #Use the matplotlib utility to open a pdf to write to to display absolute population data
    pdf = PdfPages('summary.pdf')

    #Iterate over data set to create the csv row by row and generate a graph per state
    for item in state_data:
        #Generate the prime factor
        item[str(list(item.keys())[-1]) + " Factorization"] = prime_factorization(int(item[list(item.keys())[-1]].split('(')[0]))
        #Write completed dict to csv
        output.writerow(item.values())
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.ticklabel_format(useOffset=False, style='plain')
        years = list(item.keys())[1:-1]
        pops = list(map(back_to_int, list(item.values())[1:-1]))
        plt.plot(years, pops, linestyle=None, marker='.')
        plt.xlabel("Time")
        plt.ylabel(f"Population of {item['State']}")
        pdf.savefig(fig)

    pdf.close()
    data_file.close()

main()