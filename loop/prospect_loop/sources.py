"""Lead sources. Each source yields raw lead dicts; the pipeline dedupes by domain.

To add a source: subclass `LeadSource`, implement `fetch()`, register it in `SOURCES`.
A raw lead needs at least `company` and `domain`; every other field is optional.
"""
from __future__ import annotations

import csv
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable, Iterable, Iterator, Optional

from . import config


def normalize_domain(value: str | None) -> str:
    """'https://www.Flamapp.ai/about' -> 'flamapp.ai'."""
    if not value:
        return ""
    v = value.strip().lower()
    v = re.sub(r"^[a-z]+://", "", v)
    v = v.split("/")[0].split("?")[0].split("#")[0]
    return v[4:] if v.startswith("www.") else v


class LeadSource:
    name = "base"

    def fetch(self) -> Iterable[dict]:
        raise NotImplementedError


class CsvSource(LeadSource):
    """Primary source: the Series B list shipped with the brief."""

    name = "csv"

    def __init__(self, path: Path | str | None = None):
        self.path = Path(path or config.CSV_PATH)

    def fetch(self) -> Iterator[dict]:
        with open(self.path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                contacts = []
                for i in (1, 2):
                    name = (row.get(f"Contact {i}") or "").strip()
                    if name:
                        contacts.append({
                            "name": name,
                            "title": (row.get(f"Contact {i} title") or "").strip(),
                            "linkedin": (row.get(f"Contact {i} LinkedIn URL") or "").strip(),
                        })
                yield {
                    "source": self.name,
                    "company": row["Company"].strip(),
                    "domain": row["Domain"].strip(),
                    "hq": ", ".join(x for x in (row.get("HQ City"), row.get("HQ State")) if x),
                    "round": (row.get("Latest funding round") or "").strip(),
                    "round_date_raw": (row.get("Round date") or "").strip(),
                    "round_amount_m": (row.get("Latest round ($M)") or "").strip(),
                    "total_funding_m": (row.get("Total funding ($M)") or "").strip(),
                    "funding_source": (row.get("Funding source (public knowledge)") or "").strip(),
                    "confidence_notes": (row.get("Confidence / audit") or "").strip(),
                    "what_they_do": (row.get("What they do") or "").strip(),
                    "company_linkedin": (row.get("Company LinkedIn") or "").strip(),
                    "contacts": contacts,
                }


class FundingNewsSource(LeadSource):
    """STUB: funding-news feeds (RSS/Atom) -> Series B announcements.

    Works today on any RSS feed whose item titles look like
    "<Company> raises $40M Series B ...". What is missing is domain resolution:
    a headline has a company name, not a domain, and dedupe is by domain. Plug a
    resolver in (a search API, Clearbit-style lookup, or an LLM call with web
    search) via `domain_resolver`. Without one, items whose link does not point
    at the company's own site are skipped.

    Enable with:  FUNDING_FEEDS="https://feed1.xml,https://feed2.xml"
    """

    name = "funding_news"
    TITLE_RE = re.compile(
        r"^(?P<company>[A-Z][\w.&' -]{1,60}?)\s+(?:raises|lands|secures|closes)\s+"
        r"\$(?P<amount>[\d.]+)\s*(?P<unit>[MB])\w*.*?Series\s+(?P<round>B\S*)",
        re.IGNORECASE,
    )
    NEWS_HOSTS = ("techcrunch.com", "prnewswire.com", "businesswire.com", "globenewswire.com",
                  "siliconangle.com", "finsmes.com", "reuters.com", "fortune.com", "news.google.com")

    def __init__(self, feeds: Optional[list[str]] = None,
                 domain_resolver: Optional[Callable[[str, str], Optional[str]]] = None,
                 fetcher: Optional[Callable[[str], str]] = None):
        env = os.environ.get("FUNDING_FEEDS", "")
        self.feeds = feeds if feeds is not None else [f.strip() for f in env.split(",") if f.strip()]
        self.domain_resolver = domain_resolver
        self.fetcher = fetcher or self._http_get

    @staticmethod
    def _http_get(url: str) -> str:
        req = urllib.request.Request(url, headers={"User-Agent": "prospect-loop/0.1"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", "replace")

    def parse(self, xml_text: str) -> Iterator[dict]:
        root = ET.fromstring(xml_text)
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            m = self.TITLE_RE.search(title)
            if not m:
                continue
            company = m.group("company").strip()
            domain = None
            if self.domain_resolver:
                domain = self.domain_resolver(company, link)
            elif link and not any(h in link for h in self.NEWS_HOSTS):
                domain = normalize_domain(link)
            if not domain:
                continue  # TODO: needs a domain resolver
            amount = float(m.group("amount")) * (1000 if m.group("unit").upper() == "B" else 1)
            yield {
                "source": self.name,
                "company": company,
                "domain": domain,
                "round": "Series " + m.group("round"),
                "round_date_raw": (item.findtext("pubDate") or "").strip(),
                "round_amount_m": f"{amount:g}",
                "funding_source": link,
                "what_they_do": "",
                "contacts": [],  # TODO: enrich contacts (no personal data is scraped here)
            }

    def fetch(self) -> Iterator[dict]:
        for url in self.feeds:
            try:
                yield from self.parse(self.fetcher(url))
            except Exception as exc:  # a broken feed must not stop the run
                print(f"[funding_news] skipped {url}: {exc}")


SOURCES: dict[str, type[LeadSource]] = {
    CsvSource.name: CsvSource,
    FundingNewsSource.name: FundingNewsSource,
}


def collect(source_names: Iterable[str]) -> tuple[list[dict], dict]:
    """Run sources, drop excluded domains, dedupe by normalized domain (first wins)."""
    seen: dict[str, dict] = {}
    stats = {"fetched": 0, "excluded": 0, "duplicates": 0}
    for name in source_names:
        for raw in SOURCES[name]().fetch():
            stats["fetched"] += 1
            domain = normalize_domain(raw.get("domain"))
            if not domain:
                continue
            if domain in config.EXCLUDE_DOMAINS:
                stats["excluded"] += 1
                continue
            if domain in seen:
                stats["duplicates"] += 1
                continue
            raw["domain"] = domain
            seen[domain] = raw
    return list(seen.values()), stats
