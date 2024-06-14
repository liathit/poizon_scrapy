import requests
from bs4 import BeautifulSoup
import json
import re

headers = {
    "Accept" : "*/*",
    "User-Agent" : ""
}
for page in range(1, 21):
    url = "https://www.poizon.com/category/sneakers-500000091?pinSpuIds=64839289"
    req = requests.get(url + f"&page={page}", headers=headers)
    src = req.text

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(src)


    with open ("index.html", encoding="utf-8") as file:
        src = file.read()

    bs = BeautifulSoup(src, "lxml")

    all_sneakers = []
    all_size = []

    size_mapping = {
        "3": "34.5",
        "3.5": "35.5",
        "4": "36",
        "4.5": "36.5",
        "5": "37",
        "5.5": "37.5",
        "6": "38",
        "6.5": "39",
        "7": "40",
        "7.5": "40.5",
        "8": "41",
        "8.5": "42",
        "9": "42.5",
        "9.5": "43",
        "10": "44",
        "10.5": "44.5",
        "11": "45",
        "11.5": "45.5",
        "12": "46",
        "12.5": "47",
        "13": "47.5",
        "13.5": "48",
        "14": "48.5",
        "14.5": "49",
        "15": "50",
        "15.5": "50.5",
        "16": "51",
        "16.5": "51.5",
        "17": "52",
        "17.5": "52.5",
        "18": "53",
        "18.5": "53.5",
        "19": "54",
        "19.5": "54.5",
        "20": "55",
        "20.5": "55.5",
        "21": "56",
        "21.5": "56.5",
        "22": "57",
        "/": "Out of stock",
        " ": "Out of stock"
    }

    sneakers = bs.find_all("a", class_="GoodsItem_goodsItem__pfNZb")

    for link in sneakers:
        sneakers_link = "https://www.poizon.com" + link.get("href")
        sneakers_name = link.find("div", class_="GoodsItem_spuTitle__ED79N").text
        # print(f'{sneakers_name}: {sneakers_link}')

        all_sneakers.append({"name": sneakers_name, "link": sneakers_link, "dimensions": all_size})

    with open (f"all_sneakers{page}.json", "w", encoding="utf-8") as file:
        json.dump(all_sneakers, file, indent = 4, ensure_ascii = False)

    #_________________________

    sneakers_info_list = []

    with open(f"all_sneakers{page}.json") as file:
        all_sneak_info = json.load(file)

    for sneaker_data in all_sneak_info:
        req = requests.get(url = sneaker_data["link"], headers = headers)
        src = req.text

        bs = BeautifulSoup(src, "lxml")

        price = bs.find_all("div", class_="SkuPanel_item__46ocX")

        for item in price:
            size_price = item.find("div", class_="SkuPanel_price__KCs7G")
            size = item.find("div", class_="SkuPanel_value__BAJ1p")

            if size_price is not None and size is not None:
                if "Days" not in size.text:
                    size_text = size.text.strip()
                    if size_text in size_mapping:
                        european_size = size_mapping[size_text]
                        size_price_update = re.sub(r"\$--", "Out of stock", size_price.text)
                        print(f"{european_size}: {size_price_update}")
                        sneakers_info = {
                            "size": european_size,
                            "price": size_price_update
                        }
                        sneaker_data["dimensions"].append(sneakers_info)
                    else:
                        print(f"Size mapping not found for: {size_text}")
            else:
                print("Price or size not found")
                
        sneakers_info_list.append(sneaker_data)

    with open(f"sneakers_info{page}.json", "w", encoding="utf-8") as file:
        json.dump(sneakers_info_list, file, indent=4, ensure_ascii=False)
