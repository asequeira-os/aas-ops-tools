# run as
# uv run python ops_tools/dns_fetch.py --help
# example
# uv run python ops_tools/dns_fetch.py --format text --domains github.com
import argparse
import json
from collections import defaultdict
from typing import Final, cast

import dns.rdtypes
import dns.rdtypes.ANY
import dns.rdtypes.ANY.MX
import dns.rdtypes.ANY.TXT
import dns.resolver


def get_dns_records(domain: str):
    record_types = [
        "A",
        "AAAA",
        "MX",
        "CNAME",
        "NS",
        "SOA",
        "TXT",
    ]

    resolver = dns.resolver.Resolver()
    results = {}
    for record_type in record_types:
        try:
            answer = resolver.resolve(
                domain,
                record_type,
                # tcp=True,
                lifetime=20,
            )
            results[record_type] = [unpack_rdata(rdata) for rdata in answer]
        except dns.resolver.NoAnswer:
            results[record_type] = []
        except dns.resolver.NXDOMAIN:
            results[record_type] = []
        except dns.resolver.NoNameservers:
            results[record_type] = []
        except Exception:
            raise
    return results


def unpack_rdata(rdata):
    match type(rdata):
        case dns.rdtypes.ANY.MX.MX:
            rdata = cast(dns.rdtypes.ANY.MX.MX, rdata)
            return {
                "pref": rdata.preference,
                "exchange": rdata.exchange.to_text(),
            }
        case dns.rdtypes.ANY.TXT:
            rdata = cast(dns.rdtypes.ANY.TXT, rdata)
            return [bb.decode("utf-8") for bb in rdata.strings]

    return str(rdata)


record_name_lookup: Final = {
    "A": "IPv4 Addresses",
    "AAAA": "IPv6 Addresses",
    "MX": "Mail Exchanger",
    "CNAME": "Canonical Name",
    "TXT": "Text Records",
    "NS": "Name Servers",
    "SOA": "Start of Authority",
}

TEXT = "text"
JSON = "json"


def display_results(domain: str, results, format, data):
    drec = {}
    data[domain] = drec
    if format == TEXT:
        print("-" * 60)
        print("DNS Records for {domain}")
    drec["records"] = defaultdict(list)
    for record_type, record_data in results.items():
        record_title = record_name_lookup.get(
            record_type,
            f"Unknown {record_type}",
        )
        if format == TEXT:
            print(record_title)
        if record_data:
            for record in record_data:
                if format == TEXT:
                    print(f"  - {record}")
                drec["records"][record_type].append(record)
        else:
            if format == TEXT:
                print("  No record data")


def main(args):
    _data = {}
    for domain in args.domains:
        results = get_dns_records(domain)
        display_results(
            domain,
            results,
            args.format,
            data=_data,
        )
        if args.format == JSON:
            print(json.dumps(_data, sort_keys=True, indent=2))


_arg_parser = argparse.ArgumentParser()
_arg_parser.add_argument(
    "--domains",
    metavar="S",
    type=str,
    nargs="+",
    required=True,
    help="a list of strings",
)
_arg_parser.add_argument(
    "--format",
    choices=[TEXT, JSON],
    help="Output format",
    default=TEXT,
)

if __name__ == "__main__":
    main(_arg_parser.parse_args())
