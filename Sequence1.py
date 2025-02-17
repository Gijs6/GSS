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

splits = css_data.split("}")

css_nice = []


def selectortolinenumber(selector):


    # Zoek het eerste element dat bij de selector past
    element = soup.select_one(selector)

    if element is None:
        return None  # Geen element gevonden

    # Zoek de tekst van het element in de HTML-string
    element_str = str(element)

    # Zoek de eerste regel waarin de tag voorkomt
    for i, line in enumerate(lines, start=1):
        if element_str in line:
            return i  # Lijnnummer teruggeven

    return None  # Als het element niet letterlijk in een enkele regel stond


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
        print(all_propertys_with_values_nice)
        all_propertys_with_values_nice_sorted = all_propertys_with_values_nice.sort(
            key=lambda s: int(s["oderdata"]["Index"]) if s.get("oderdata") and s["oderdata"].get("Index") else float(
                'inf')
        )

        css_nice.append({
            "selector": selectorstuff,
            "selectorsort": selectortolinenumber(selectorstuff),
            "styles": all_propertys_with_values_nice_sorted
        })

print(css_data)
print()
print(json.dumps(css_nice, indent=4))
css_data_sorted = css_nice.sort(key=lambda s: int(s["selectorsort"]) if s.get("selectorsort") else float('inf'))

open = "{"
close = "}"

for item in css_data_sorted:
    print(f"{item['selector']} {open}")
    for style in item["styles"]:
        print(f"    {style['property']}")
    print(close)
    print("")