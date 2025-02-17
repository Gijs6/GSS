import json
from bs4 import BeautifulSoup
import re

with open("testdata.css") as file:
    css_data = file.read()

with open("testdata.html", encoding="utf-8") as file:
    html_content = file.read()


lines = html_content.splitlines()

# Parse and prettify
soup = BeautifulSoup(html_content, "html.parser")
css_data = "".join(css_data.splitlines())
htmlcontentstuff429 = soup.decode(formatter="html")
htmldatastuff = "".join([line.strip() for line in str(soup).splitlines()]).replace('\n', '').replace('\r', '')
print(htmldatastuff)

splits = css_data.split("}")

css_nice = []


def selectortolinenumber(selector):
    element = soup.select_one(selector)

    if not element:
        return None



    print("---")
    print(f"Element {element}")
    print(f"et {type(element)}")
    print(f"strel {str(element)}")
    print(f"Element2 {str(element).replace('\n', '').replace('\r', '')}")


    indexstuff = htmldatastuff.find(str(element).replace('\n', '').replace('\r', '').strip())

    print(f"Indexstuffstuff {indexstuff}")
    print("---")

with open("order.json") as orderfile:
    orderdata = json.load(orderfile)

for item in splits:
    if item:
        itemsplits = item.split("{")
        selectorstuff = itemsplits[0].strip()
        propertys_with_values = itemsplits[1]
        all_propertys_with_values_together = [item.strip() for item in propertys_with_values.split(";") if item]
        all_propertys_with_values_nice = []
        for propwithvalue in all_propertys_with_values_together:
            itemsplitstuff = propwithvalue.split(":")
            prop_this_prop = itemsplitstuff[0].strip()
            all_propertys_with_values_nice.append({
                "property": prop_this_prop,
                "value": itemsplitstuff[1].strip(),
                "oderdata": orderdata.get(prop_this_prop)
            })
        all_propertys_with_values_nice_sorted = all_propertys_with_values_nice.sort(
            key=lambda s: int(s["oderdata"]["Index"]) if s.get("oderdata") and s["oderdata"].get("Index") else float(
                'inf')
        )

        css_nice.append({
            "selector": selectorstuff,
            "selectorsort": selectortolinenumber(selectorstuff),
            "styles": all_propertys_with_values_nice_sorted
        })

css_data_sorted = css_nice.sort(key=lambda s: int(s["selectorsort"]) if s.get("selectorsort") else float('inf'))

open = "{"
close = "}"