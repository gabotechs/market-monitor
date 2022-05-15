from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    ticker: str,
    *,
    client: Client,
    comparisons: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    region: Union[Unset, None, str] = UNSET,
    interval: Union[Unset, None, str] = UNSET,
    lang: Union[Unset, None, str] = UNSET,
    events: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v8/finance/chart/{ticker}".format(client.base_url, ticker=ticker)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["comparisons"] = comparisons

    params["range"] = range_

    params["region"] = region

    params["interval"] = interval

    params["lang"] = lang

    params["events"] = events

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
    ticker: str,
    *,
    client: Client,
    comparisons: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    region: Union[Unset, None, str] = UNSET,
    interval: Union[Unset, None, str] = UNSET,
    lang: Union[Unset, None, str] = UNSET,
    events: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get chart data by ticker

    Args:
        ticker (str):  Example: AAPL.
        comparisons (Union[Unset, None, str]):  Example: MSFT,^VIX.
        range_ (Union[Unset, None, str]):  Example: 1mo.
        region (Union[Unset, None, str]):  Example: US.
        interval (Union[Unset, None, str]):  Example: 1d.
        lang (Union[Unset, None, str]):  Example: en.
        events (Union[Unset, None, str]):  Example: div,split.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
        client=client,
        comparisons=comparisons,
        range_=range_,
        region=region,
        interval=interval,
        lang=lang,
        events=events,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    ticker: str,
    *,
    client: Client,
    comparisons: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    region: Union[Unset, None, str] = UNSET,
    interval: Union[Unset, None, str] = UNSET,
    lang: Union[Unset, None, str] = UNSET,
    events: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get chart data by ticker

    Args:
        ticker (str):  Example: AAPL.
        comparisons (Union[Unset, None, str]):  Example: MSFT,^VIX.
        range_ (Union[Unset, None, str]):  Example: 1mo.
        region (Union[Unset, None, str]):  Example: US.
        interval (Union[Unset, None, str]):  Example: 1d.
        lang (Union[Unset, None, str]):  Example: en.
        events (Union[Unset, None, str]):  Example: div,split.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
        client=client,
        comparisons=comparisons,
        range_=range_,
        region=region,
        interval=interval,
        lang=lang,
        events=events,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
