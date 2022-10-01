"""API Call to Shopify."""
import time
import re
from configparser import SectionProxy
from typing import Union, Tuple, Optional
import requests
from requests import Response
from requests.utils import CaseInsensitiveDict


def header_link(hdr: CaseInsensitiveDict) -> Tuple[Optional[str], int]:
    """Get next page link from header response."""
    next_url = None
    if hdr is not None and hdr.get('link') is not None:
        link_ls = hdr['link'].split(", ")
        for lnk in link_ls:
            if 'next' in lnk:
                link_rel = re.search(r'^<(\S*)>', lnk)
                if link_rel is None:
                    continue
                next_url = link_rel.group(1)
    retry = hdr.get('Retry-After', 0)
    return next_url, retry


def api_call(next_url: str, shop_conf: SectionProxy,
             init_params: dict = None, page: bool = True
             ) -> Union[Response, None]:
    """Call Shopify API."""
    shop_hdr = {'Content-Type': 'application/json',
                'X-Shopify-Access-Token': shop_conf.get('access_token')}
    max_calls = 10
    call_num = 0
    while call_num < max_calls:
        call_num += 1
        if not page:
            resp = requests.get(url=next_url, headers=shop_hdr,
                                params=init_params, timeout=30)
        else:
            resp = requests.get(url=next_url, headers=shop_hdr, timeout=30)
        if resp.status_code == 429:
            retry = resp.headers.get('Retry-After', 2)
            time.sleep(int(retry) * call_num)
        resp.raise_for_status()
        if resp.status_code == 200:
            return resp
    return None
