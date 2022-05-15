from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    region: Union[Unset, None, str] = UNSET,
    lang: Union[Unset, None, str] = UNSET,
    query: str,
) -> Dict[str, Any]:
    url = "{}/v6/finance/autocomplete".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["region"] = region

    params["lang"] = lang

    params["query"] = query

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
    query: str,
) -> Response[Any]:
    """Get auto complete stock suggestions

    Args:
        region (Union[Unset, None, str]):  Example: US.
        lang (Union[Unset, None, str]):  Example: en.
        query (str):  Example: apple.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        region=region,
        lang=lang,
        query=query,
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
    query: str,
) -> Response[Any]:
    """Get auto complete stock suggestions

    Args:
        region (Union[Unset, None, str]):  Example: US.
        lang (Union[Unset, None, str]):  Example: en.
        query (str):  Example: apple.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        region=region,
        lang=lang,
        query=query,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
