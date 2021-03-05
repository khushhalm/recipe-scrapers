# southernliving.com scraper
# Written by G.D. Wallters
# Freely released the code to recipe_scraper group
# 9 February, 2020
# =======================================================
from ._abstract import AbstractScraper
from ._utils import get_minutes, get_yields, normalize_string


class SouthernLiving(AbstractScraper):
    @classmethod
    def host(cls):
        return "southernliving.com"

    def title(self):
        return normalize_string(self.soup.find("h1").get_text())

    def total_time(self):
        total_time = 0
        try:
            tt1 = self.soup.findAll("div", {"class": "recipe-meta-item"})
            for tt in tt1:
                # Find the entry that has 'Total'
                header = normalize_string(
                    tt.find("div", {"class": "recipe-meta-item-header"}).get_text()
                )
                if "total" in header.lower():
                    total_time = normalize_string(
                        tt.find("div", {"class": "recipe-meta-item-body"}).get_text()
                    )
                    break

        except Exception:
            tt1 = 0
        total = get_minutes(total_time)
        return total

    def yields(self):
        try:
            yield1 = self.soup.findAll("div", {"class": "recipe-meta-item"})
            for y in yield1:
                # Find the entry that has 'Yield'
                header = normalize_string(
                    y.find("div", {"class": "recipe-meta-item-header"}).get_text()
                )
                if header == "Yield":
                    y = normalize_string(
                        y.find("div", {"class": "recipe-meta-item-body"}).get_text()
                    )
                    break
        except Exception:
            y = 0
        total = get_yields(y)
        return total

    def image(self):
        try:
            image = self.soup.find(
                "div", {"class": "image-container"}
            )  # , 'src': True})
            im = image.find(
                "div",
                attrs={"class": lambda e: e.startswith("component") if e else False},
            )

            lnk = im["data-src"]
        except Exception:
            lnk = None

        return lnk  # if image else None

    def ingredients(self):
        ingredientsOuter = self.soup.find("ul", {"class": "ingredients-section"})
        lines = ingredientsOuter.findAll("li")

        return [normalize_string(li.label.get_text()) for li in lines]

    def instructions(self):
        instructions = self.soup.find("ul", {"class": "instructions-section"})

        data = []
        instruction = instructions.findAll("li", {"class": "instructions-section-item"})
        for ins in instruction:
            line = normalize_string(ins.find("div", {"class": "paragraph"}).get_text())
            data.append(line)
        return data

    def ratings(self):
        # This site does not support ratings at this time
        r1 = None
        return r1

    def description(self):
        des = self.soup.find(
            "div",
            attrs={"class": lambda e: e.startswith("recipe-summary") if e else False},
        )
        d = normalize_string(des.get_text())

        return d if d else None
