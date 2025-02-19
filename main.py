import json
from bs4 import BeautifulSoup


def mainGSS(htmlinput, cssinput):
    css_data = cssinput
    html_content = htmlinput

    soup = BeautifulSoup(html_content, "html.parser")
    css_data = "".join(css_data.splitlines())
    htmldatastuff = "".join([line.strip() for line in str(soup).splitlines()]).replace('\n', '').replace('\r', '')

    with open("order.json") as orderfile:
        orderdata = json.load(orderfile)

    def format_css2(inputdata):
        rm_statements = []

        statements = re.findall(r'@\w+[^;{]*;', inputdata)
        rm_statements.extend(statements)
        inputdata = re.sub(r'@\w+[^;{]*;', '', inputdata)

        rm_blocks = []

        blocks = re.findall(r'@[\w-]+\s*[^{}]*\{(?:[^{}]|\{[^{}]*\})*\}', inputdata, flags=re.DOTALL)
        rm_blocks.extend(blocks)
        inputdata = re.sub(r'@[\w-]+\s*[^{}]*\{(?:[^{}]|\{[^{}]*\})*\}', '', inputdata, flags=re.DOTALL)

        inputdata = re.sub(r'/\*.*?\*/', '', inputdata, flags=re.DOTALL)

        return inputdata, rm_statements, rm_blocks


    def selectortolinenumber(selector):
        if "webkit" in selector or "moz" in selector:
            return 10000000
        elif "::" in selector or ":root" in selector:
            return 0
        elif ":hover" in selector:
            element = soup.select_one(selector.replace(":hover", ""))
            hoverorderstuff = 1
        else:
            logging.error(selector)
            element = soup.select_one(selector)
            hoverorderstuff = 0

        if not element:
            return 1000000

        indexstuff = htmldatastuff.find(
            "".join([line.strip() for line in str(element).splitlines()]).replace('\n', '').replace('\r', ''))

        return indexstuff + hoverorderstuff


    def css_in_order(css_input_data):
        css_no_at, rm_statements, rm_blocks = format_css2(css_input_data)

        splits = css_no_at.split("}")
        css_nice = []



        for item in splits:
            if item:
                logging.error(f"item {item}")
                itemsplits = item.split("{")
                selectorstuff = itemsplits[0].strip()
                propertys_with_values = itemsplits[1].strip()
                all_propertys_with_values_together = [item.strip() for item in propertys_with_values.split(";") if item]
                all_propertys_with_values_nice = []
                for propwithvalue in all_propertys_with_values_together:
                    logging.error(f"propwithvalue {propwithvalue}")
                    itemsplitstuff = propwithvalue.split(":")
                    prop_this_prop = itemsplitstuff[0].strip()
                    all_propertys_with_values_nice.append({
                        "property": prop_this_prop,
                        "value": itemsplitstuff[1].strip(),
                        "oderdata": orderdata.get(prop_this_prop, {"Cat": "10000", "Index": "10000"})
                    })

                all_propertys_with_values_nice_sorted = sorted(all_propertys_with_values_nice, key=lambda s: int(s["oderdata"]["Index"]))

                css_nice.append({
                    "selector": selectorstuff,
                    "selectorsort": selectortolinenumber(selectorstuff),
                    "styles": all_propertys_with_values_nice_sorted
                })

        css_data_sorted = sorted(css_nice, key=lambda s: s["selectorsort"])

        return css_data_sorted, rm_statements, rm_blocks



    css_data_sorted, removed_statements, removed_blocks = css_in_order(css_data)

    css_output = ""

    css_output_end = "\n\n"

    for atblock in removed_statements:
        css_output += atblock + "\n\n"

    for atblock in removed_blocks:
        if "media" in atblock:
            reeegeks_media_block = re.search(r'@media\s*([^{]+)\s*{(.*)}\s*$', atblock, re.DOTALL)
            media_condition = reeegeks_media_block.group(1).strip()
            media_styles = reeegeks_media_block.group(2).strip()
            media_data = "".join(media_styles.splitlines())
            media_data_sorted, removed_statements_media, removed_blocks_media = css_in_order(media_data)
            css_output_end += f"@media {media_condition} {{\n"
            for block in media_data_sorted:
                css_output_end += f"    {block['selector']} {{\n"
                for style in block["styles"]:
                    css_output_end += f"       {style['property']}: {style['value']};\n"
                css_output_end += "    }\n\n"
            css_output_end += "}\n\n"
        else:
            css_output_end += atblock + "\n"


    for block in css_data_sorted:
        css_output += f"{block['selector']} {{\n"
        for style in block["styles"]:
            css_output += f"   {style['property']}: {style['value']};\n"
        css_output += "}\n\n"

    final_css = css_output + css_output_end

    return final_css





if __name__ == "__main__":
    with open("testdata/testdata.css") as file:
        css_data = file.read()
    with open("testdata/testdata.html", encoding="utf-8") as file:
        html_data = file.read()
    
    print(mainGSS(css_data, html_data))
