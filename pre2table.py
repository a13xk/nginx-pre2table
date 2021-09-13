import sys
from typing import List

from bs4 import BeautifulSoup, Tag

from requests import (
    get,
    Response
)


def main():
    if len(sys.argv) != 2:
        raise ValueError("Pass URL as script parameter")
    url: str = sys.argv[1]
    if not url.startswith("http"):
        raise ValueError("Pass valid URL as script parameter")
    if not url.endswith("/"):
        url = f"{url}/"
    report_filename: str = f'{url.rstrip("/").split(sep="/")[-1]}.html'

    response: Response = get(url=url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(markup=response.text, features="html.parser")

        pre_tag: Tag = soup.find(name="pre")
        all_a_tags: List[Tag] = soup.find_all(name="a")
        all_hrefs: List[str] = [a_tag.attrs.get("href") for a_tag in all_a_tags]
        dates_and_sizes: List[Tag] = [a_tag.next_sibling for a_tag in all_a_tags]
        new_dates_and_sizes: List[dict] = [{"date": None, "time": None, "size": None}]
        for ds in dates_and_sizes:
            ds = str(ds).strip()
            if ds:
                date = ds.split()[0]
                time = ds.split()[1]
                size = ds.split()[-1]
                new_dates_and_sizes.append(
                    {"date": date, "time": time, "size": size}
                )
        all_full_hrefs = [f"{url}{href}" for href in all_hrefs]

        table: Tag = soup.new_tag(name="table", style="font-family: monospace")

        table_header: Tag = soup.new_tag(name="thead")
        table_header_row: Tag = soup.new_tag(name="tr")
        td: Tag = soup.new_tag(name="td")
        td.string = "Filename"
        table_header_row.append(tag=td)
        td: Tag = soup.new_tag(name="td")
        td.string = "Date/Time"
        table_header_row.append(tag=td)
        td: Tag = soup.new_tag(name="td")
        td.string = "Size"
        table_header_row.append(tag=td)
        table_header.append(tag=table_header_row)

        table_body: Tag = soup.new_tag(name="tbody")
        for href, full_href, date_size in zip(all_hrefs, all_full_hrefs, new_dates_and_sizes):
            table_row: Tag = soup.new_tag(name="tr")

            td: Tag = soup.new_tag(name="td")
            a: Tag = soup.new_tag(name="a", href=full_href)
            a.string = href
            td.append(tag=a)
            table_row.append(tag=td)

            date_time: str = f'{date_size.get("date")} {date_size.get("time")}'
            if "None" in date_time:
                date_time = ""
            td: Tag = soup.new_tag(name="td")
            td.string = date_time
            table_row.append(tag=td)

            size: str = f'{date_size.get("size")}'
            if "None" in size:
                size = ""
            td: Tag = soup.new_tag(name="td")
            td.string = size
            table_row.append(tag=td)

            table_body.append(table_row)

        table.append(tag=table_header)
        table.append(tag=table_body)

        pre_tag.insert_after(table)
        pre_tag.decompose()

        with open(file=report_filename, mode="w", encoding="utf-8") as f:
            s = str(soup)
            f.write(s)
#


if __name__ == '__main__':
    main()
#

