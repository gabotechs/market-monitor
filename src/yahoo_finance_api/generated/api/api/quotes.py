from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    region: Union[Unset, None, str] = UNSET,
    lang: Union[Unset, None, str] = UNSET,
    symbols: str,
) -> Dict[str, Any]:
    url = "{}/v6/finance/quote".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["region"] = region

    params["lang"] = lang

    params["symbols"] = symbols

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    region: Union[Unset, None, str] = UNSET,
    lang: Union[Unset, None, str] = UNSET,
    symbols: str,
) -> Response[Any]:
    """Real time quote data for stocks, ETFs, mutuals funds, etc…

    Args:
        region (Union[Unset, None, str]):  Example: US.
        lang (Union[Unset, None, str]):  Example: en.
        symbols (str):  Example: AAPL,BTC-USD,EURUSD=X.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        region=region,
        lang=lang,
        symbols=symbols,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    region: Union[Unset, None, str] = UNSET,
    lang: Union[Unset, None, str] = UNSET,
    symbols: str,
) -> Response[Any]:
    """Real time quote data for stocks, ETFs, mutuals funds, etc…

    Args:
        region (Union[Unset, None, str]):  Example: US.
        lang (Union[Unset, None, str]):  Example: en.
        symbols (str):  Example: AAPL,BTC-USD,EURUSD=X.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        region=region,
        lang=lang,
        symbols=symbols,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
