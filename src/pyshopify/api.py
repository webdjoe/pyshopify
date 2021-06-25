"""API Call to Shopify."""
from typing import Union, Tuple
import re
import requests
from configparser import SectionProxy
from requests import Response
from requests.utils import CaseInsensitiveDict


def header_link(hdr: CaseInsensitiveDict) -> Tuple[str, int]:
    """Get next page link from header response."""
    next_url = None
    if hdr is not None and hdr.get('link') is not None:
        link_ls = hdr.get('link').split(", ")
        for lnk in link_ls:
            if 'next' in lnk:
                link_rel = re.search('^<(\S*)>', lnk)
                next_url = link_rel.group(1)
    retry = hdr.get('Retry-After', 0)
    return next_url, retry


def api_call(next_url: str, shop_conf: SectionProxy, init_params: dict = None, page: bool =True) -> Union[Response, None]:
    """Call Shopify API."""
    shop_hdr = {'Content-Type': 'application/json',
                'X-Shopify-Access-Token': shop_conf.get('access_token')}
    if not page:
        resp = requests.get(url=next_url, headers=shop_hdr,
                            params=init_params)
    else:
        resp = requests.get(url=next_url, headers=shop_hdr)
    if resp.status_code != 200:
        return None
    return resp
