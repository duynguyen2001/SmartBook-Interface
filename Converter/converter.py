import json
import re
from urllib.parse import urlparse
from datetime import datetime
import os


def ensure_dir(directory):
    """Check if a directory exists, and if not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} was created.")
    else:
        print(f"Directory {directory} already exists.")


def ordinal_suffix(day):
    """Returns the ordinal suffix for a day in the month (e.g., 'st', 'nd', 'rd', 'th')"""
    if 10 <= day <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return suffix


def convert_iso_to_date(iso_string):
    # Parse the ISO string to a datetime object
    if iso_string == "None":
        return ""
    date_obj = datetime.fromisoformat(iso_string)
    day = date_obj.day
    return (
        date_obj.strftime("%b ")
        + str(day)
        + ordinal_suffix(day)
        + date_obj.strftime(", %Y")
    )


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = re.sub(r"^(https?:\/\/)?(www\.)?", "", parsed_url.netloc)
    return domain


def split_and_format_summary(summary):
    formatted_summary = ""
    parts = re.split("(\([\d+, ]+\))", summary)
    for part_id, part in enumerate(parts):
        if part_id % 2 == 1:
            # Extracting numbers and formatting them as HTML links
            numbers = part.strip("()").split(", ")
            formatted_links = ", ".join(
                [
                    ", ".join(
                        [f'<a href="#{num}">{num}</a>' for num in nums.split(",")]
                    )
                    for nums in numbers
                ]
            )
            formatted_summary += f"<font color=#FF3399>[{formatted_links}]</font>"
        else:
            formatted_summary += part
    return formatted_summary.replace("\n", "<br/>")


def create_markdown_from_json(
    cfg_name,
    file_name,
    big_title,
    dump_path,
    data_dump_dir_name,
    side_ratings_file_name,
):
    # Loading data
    with open(file_name, "r") as f:
        data = json.load(f)

    # Creating dump directory
    ensure_dir(dump_path + data_dump_dir_name)

    # Loading files
    try:
        with open(dump_path + cfg_name, "r") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = {"data": []}

    side_ratings_dict = {}
    # Loading side ratings
    with open(side_ratings_file_name, "r") as f:
        side_ratings_json = json.load(f)
        side_ratings = side_ratings_json["allsides_media_bias_ratings"]
        for rating in side_ratings:
            site = rating["publication"]
            side_ratings_dict[get_domain_name(site["source_url"])] = site

    # Adding side ratings
    cfg_sections = []
    for cluster in data:
        cfg_section = {"title": cluster["cluster_headline"], "sections": []}
        # create a source dictionary
        article_map = {}
        for article in cluster["all_articles"]:
            article_map[article["link"]] = article
        for question, claims_data in cluster["questions"].items():
            md_text = "# {}\n\n## Summary\n<DetailSlider>\n".format(question)

            # Formatting summaries
            md_text += "<template v-slot:less-detailed>\n{}\n</template>\n".format(
                split_and_format_summary(claims_data["less_detailed"])
            )
            md_text += "<template v-slot:summary>\n{}\n</template>\n".format(
                split_and_format_summary(claims_data["summary"])
            )
            md_text += "<template v-slot:more-detailed>\n{}\n</template>\n</DetailSlider>\n".format(
                split_and_format_summary(claims_data["more_detailed"])
            )

            # Adding claims
            md_text += (
                "\n## Claims\n| Claim Sentence | Source | Context |\n|---|---|---|\n"
            )
            for claim_id, claim in enumerate(claims_data["claims"]):
                if get_domain_name(claim["link"]) in side_ratings_dict:
                    source = side_ratings_dict[get_domain_name(claim["link"])]
                else:
                    source = {
                        "source_name": get_domain_name(claim["link"]),
                        "media_bias_rating": "N/A",
                        "source_type": "",
                        "allsides_url": "",
                    }
                sourcetype = (
                    f"*({source['source_type']})*" if source["source_type"] else ""
                )
                # get source information
                source_info = article_map[claim["link"]]
                source_date = convert_iso_to_date(source_info["date"])
                md_text += '|<font id="{}" color=#FF3399>[{}]</font> {}|<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;"><a href="{}" target="_blank"><BiasChart bias="{}" /></a><div><a href="{}" target="_blank">{}</a></div><div>{}</div><div>{}</div></div>|{}|\n'.format(
                    claim_id + 1,
                    claim_id + 1,
                    claim["sentence"],
                    source["allsides_url"],
                    source["media_bias_rating"],
                    claim["link"],
                    source["source_name"],
                    sourcetype,
                    source_date,
                    claim["context"],
                )

            file_path = "{}/{}_{}.md".format(
                data_dump_dir_name,
                file_name.replace(".", "_"),
                question.replace(" ", "_").replace(".", "_").replace("?", "_")[:30],
            )

            with open(dump_path + file_path, "w") as f:
                f.write(md_text)

            cfg_section["sections"].append(
                {
                    "id": file_path.replace(".md", ""),
                    "title": question,
                    "url": file_path,
                }
            )

        cfg_sections.append(cfg_section)

    cfg["data"] = [{"title": big_title, "sections": cfg_sections}] + cfg["data"]
    with open(dump_path + cfg_name, "w") as f:
        json.dump(cfg, f, indent=4)


# Usage
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_sept_1_15.json",
    "Sept 1st to 15th",
    "./",
    "Sept 1st to 15th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_sept_16_30.json",
    "Sept 16th to 30th",
    "./",
    "Sept 16th to 30th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_oct_1_15.json",
    "Oct 1st to 15th",
    "./",
    "Oct 1st to 15th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_oct_16_30.json",
    "Oct 16th to 30th",
    "./",
    "Oct 16th to 30th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_nov_1_15.json",
    "Nov 1st to 15th",
    "./",
    "Nov 1st to 15th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_nov_16_30.json",
    "Nov 16th to 30th",
    "./",
    "Nov 16th to 30th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_dec_1_15.json",
    "Dec 1st to 15th",
    "./",
    "Dec 1st to 15th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_dec_16_30.json",
    "Dec 16th to 30th",
    "./",
    "Dec 16th to 30th",
    "all_sides_ratings.json",
)
create_markdown_from_json(
    "vbcfg-july.json",
    "claim_summaries_gpt4_cite_jan_1_15.json",
    "Jan 1st to 15th",
    "./",
    "Jan 1st to 15th",
    "all_sides_ratings.json",
)
