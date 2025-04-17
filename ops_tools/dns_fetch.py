import argparse
from typing import Final

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
            answer = resolver.resolve(domain, record_type)
            results[record_type] = [str(rdata) for rdata in answer]
        except dns.resolver.NoAnswer:
            results[record_type] = []
        except dns.resolver.NXDOMAIN:
            results[record_type] = []
        except dns.resolver.NoNameservers:
            results[record_type] = []
        except Exception as e:
            results[record_type] = str(e)
    return results


record_name_lookup: Final = {
    "A": "IPv4 Addresses",
    "AAAA": "IPv6 Addresses",
    "MX": "Mail Exchanger",
    "CNAME": "Canonical Name",
    "TXT": "Text Records",
    "NS": "Name Servers",
    "SOA": "Start of Authority",
}


def display_results(domain, results):
    print("-" * 60)
    print("DNS Records for {domain}")
    for record_type, record_data in results.items():
        record_title = record_name_lookup.get(record_type, f"Unknown {record_type}")
        print(record_title)
        if record_data:
            for record in record_data:
                print(f"  - {record}")
        else:
            print("  No record data")


_arg_parser = argparse.ArgumentParser()
_arg_parser.add_argument(
    "--domains",
    metavar="S",
    type=str,
    nargs="+",
    required=True,
    help="a list of strings",
)

if __name__ == "__main__":
    for domain in _arg_parser.parse_args().domains:
        results = get_dns_records(domain)
        display_results(domain, results)
