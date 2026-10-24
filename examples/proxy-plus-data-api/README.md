# Proxy + data API example

Use an [IPFoxy](https://www.ipfoxy.com/) proxy for your own requests and the EveryInfra data API for structured data, in one Python script.

- **Your own requests** (a crawler or browser automation that must open a page as a user in a given country) go out through the proxy.
- **The EveryInfra call** goes direct to `api.everyinfra.com`. It does not need a proxy, and a proxy only adds proxy traffic.

Docs: [Use with IPFoxy proxies](https://everyinfra.com/en/docs#with-proxy) · [中文：配合 IPFoxy 代理使用](https://everyinfra.com/docs#with-proxy) · [Español: Uso con proxies de IPFoxy](https://everyinfra.com/es/docs#with-proxy)

## Files

| File | What it does |
|---|---|
| `proxy_plus_data_api.py` | Step 1: get `https://ipinfo.io/json` through the proxy and print the exit country. Step 2: call `POST /api/v1/social` direct for one Amazon product (`amazon` / `profile`). |
| `mock_proxy.py` | A local HTTP proxy that checks Basic auth and tunnels `CONNECT`. Use it to test the example without a proxy account. |
| `measure_page_weight.mjs` | Measures the bytes on the wire for a page in headless Chrome, so you can estimate proxy traffic per page. |
| `requirements.txt` | `requests==2.34.2` |
| `data/amazon-page-weight-2026-10-24.csv` | Raw measurements: 40 Amazon product page requests, 3 search page requests and 8 headless Chrome loads (2026-10-24, 18:30–18:41 SGT, Singapore broadband, no proxy). |
| `data/make_figs.py` | Rebuilds the three blog charts from the CSV and the IPFoxy list prices (light and dark, en / zh / es). |

## Run

```bash
pip install -r requirements.txt
export EVERYINFRA_API_KEY="<API Key>"
export IPFOXY_PROXY="http://username:password@host:port"   # from the IPFoxy dashboard
python3 proxy_plus_data_api.py
```

`direct.trust_env = False` makes the EveryInfra call ignore `HTTP_PROXY` and `HTTPS_PROXY`, so it uses no proxy traffic even when a system-wide proxy is set.

The IPFoxy help center notes that the proxy works only when the code runs from a network outside mainland China ([Python setup guide](https://www.ipfoxy.com/help/docs/bn3BDn)).

## Test without a proxy account

```bash
python3 mock_proxy.py demo s3cret 18089 &          # user, password, port
IPFOXY_PROXY="http://demo:s3cret@127.0.0.1:18089" \
HTTPS_PROXY="http://demo:s3cret@127.0.0.1:18089" \
python3 proxy_plus_data_api.py
```

What we saw on 2026-10-24 (Singapore time):

- Correct password: the mock logged `CONNECT ipinfo.io:443 | auth ok`. The EveryInfra call returned the product and was charged $0.001389. The mock did not log the EveryInfra request, although `HTTPS_PROXY` pointed to the mock.
- Wrong password: the mock returned `407`, `requests` raised `ProxyError`, and the script stopped before the EveryInfra call. Nothing was charged.

We did not have an IPFoxy account for this test, so only the mock proxy was used.

## Measure proxy traffic per page

```bash
node measure_page_weight.mjs "https://www.amazon.com/dp/B0CYJDVT31"
BLOCK=1 node measure_page_weight.mjs "https://www.amazon.com/dp/B0CYJDVT31"   # block images and fonts
```

Our numbers for Amazon product pages, the cost per 1,000 pages at each IPFoxy plan and the raw CSV are in [How Much Proxy Traffic Does an Amazon Page Use?](https://everyinfra.com/en/blog/proxy-traffic-cost-amazon-product-pages). Read the robots.txt and the terms of a site before you collect from it.
