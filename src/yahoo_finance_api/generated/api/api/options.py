from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    symbol: str,
    *,
    client: Client,
    date: Union[Unset, None, float] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v7/finance/options/{symbol}".format(client.base_url, symbol=symbol)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["date"] = date

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
    symbol: str,
    *,
    client: Client,
    date: Union[Unset, None, float] = UNSET,
) -> Response[Any]:
    """Get option chain for a particular symbol

    Args:
        symbol (str):  Example: AAPL.
        date (Union[Unset, None, float]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        symbol=symbol,
        client=client,
        date=date,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    symbol: str,
    *,
    client: Client,
    date: Union[Unset, None, float] = UNSET,
) -> Response[Any]:
    """Get option chain for a particular symbol

    Args:
        symbol (str):  Example: AAPL.
        date (Union[Unset, None, float]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        symbol=symbol,
        client=client,
        date=date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
