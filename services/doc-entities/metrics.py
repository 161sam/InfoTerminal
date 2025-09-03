from prometheus_client import Counter, REGISTRY

def get_or_create_counter(name: str, doc: str) -> Counter:
    # nutzt die (private) Registry-Map, ist für Dev/Reload absolut ok
    existing = REGISTRY._names_to_collectors.get(name)
    if existing and isinstance(existing, Counter):
        return existing
    return Counter(name, doc)

RESOLVER_RUNS = get_or_create_counter("resolver_runs", "Number of resolver runs")
RESOLVER_ENTS = get_or_create_counter("resolver_ents", "Number of entities resolved")
RESOLVER_LAT  = get_or_create_counter("resolver_latency_ms", "Latency of resolver in ms")
