import requests
import csv
from utils import get_change, prime_factorization, back_to_int, back_to_float
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main():
    BASE_URL="https://datausa.io/api/data?drilldowns=State&measures=Population"

    response = requests.get(BASE_URL).json()['data']
    seen = {}
    state_data = []

    for row in reversed(response):
        if row['Slug State'] in seen:
            seen[row['Slug State']] += 1
            state_index = next((index for (index, d) in enumerate(state_data) if d["State"] == row['State']), None)
            last_year = state_data[state_index][row['ID Year'] - 1].split('(')[0]
            this_year = row['Population']
            change = get_change(this_year, float(last_year))
            state_data[state_index][row['ID Year']] = str(row['Population']) + str(f"({change:.2f}%)")
        else:
            seen[row['Slug State']] = 1
            state_data.append({"State" : row['State'], row['ID Year'] : str(row['Population'])})
    for entry in state_data:
        entry[str(list(entry.keys())[-1]) + " Factorization"] = prime_factorization(int(entry[list(entry.keys())[-1]].split('(')[0]))

    data_file = open('./output/data_file.csv', 'w')
    output = csv.writer(data_file)
    output.writerow(state_data[0].keys())

    pdf = PdfPages('./output/Report:State_Population.pdf')
    for item in state_data:
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