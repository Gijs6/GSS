import json

with open("testdata.css") as file:
    css_data = file.read()

css_data = "".join(css_data.splitlines())

splits = css_data.split("}")

css_nice = []


with open("order.json") as orderfile:
    orderdata = json.load(orderfile)

print(orderdata.get("font-size".lower()))

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
            "styles": all_propertys_with_values_nice_sorted
        })

print(css_data)
print()
print(json.dumps(css_nice, indent=4))