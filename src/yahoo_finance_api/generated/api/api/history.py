from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    interval: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    symbols: str,
) -> Dict[str, Any]:
    url = "{}/v8/finance/spark".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["interval"] = interval

    params["range"] = range_

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
    interval: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    symbols: str,
) -> Response[Any]:
    """Stock history

    Args:
        interval (Union[Unset, None, str]):  Example: 1d.
        range_ (Union[Unset, None, str]):  Example: 1mo.
        symbols (str):  Example: AAPL,MSFT.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        interval=interval,
        range_=range_,
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
    interval: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    symbols: str,
) -> Response[Any]:
    """Stock history

    Args:
        interval (Union[Unset, None, str]):  Example: 1d.
        range_ (Union[Unset, None, str]):  Example: 1mo.
        symbols (str):  Example: AAPL,MSFT.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        interval=interval,
        range_=range_,
        symbols=symbols,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
