from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    symbol: str,
    *,
    client: Client,
    lang: Union[Unset, None, str] = UNSET,
    region: Union[Unset, None, str] = UNSET,
    modules: str,
) -> Dict[str, Any]:
    url = "{}/v11/finance/quoteSummary/{symbol}".format(client.base_url, symbol=symbol)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["lang"] = lang

    params["region"] = region

    params["modules"] = modules

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
    lang: Union[Unset, None, str] = UNSET,
    region: Union[Unset, None, str] = UNSET,
    modules: str,
) -> Response[Any]:
    """Get very detailed information for a particular stock.

    The next portions of data can be retrieved with the service:
    `summaryDetail` `assetProfile` `fundProfile` `financialData` `defaultKeyStatistics` `calendarEvents`
    `incomeStatementHistory` `incomeStatementHistoryQuarterly` `cashflowStatementHistory`
    `balanceSheetHistory` `earnings` `earningsHistory` `insiderHolders` `cashflowStatementHistory`
    `cashflowStatementHistoryQuarterly` `insiderTransactions` `secFilings` `indexTrend` `sectorTrend`
    `earningsTrend` `netSharePurchaseActivity` `upgradeDowngradeHistory` `institutionOwnership`
    `recommendationTrend` `balanceSheetHistory` `balanceSheetHistoryQuarterly` `fundOwnership`
    `majorDirectHolders` `majorHoldersBreakdown`, `price`, `quoteType`, `esgScores`

    Args:
        symbol (str):  Example: AAPL.
        lang (Union[Unset, None, str]):  Example: en.
        region (Union[Unset, None, str]):  Example: US.
        modules (str):  Example: defaultKeyStatistics,assetProfile.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        symbol=symbol,
        client=client,
        lang=lang,
        region=region,
        modules=modules,
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
    lang: Union[Unset, None, str] = UNSET,
    region: Union[Unset, None, str] = UNSET,
    modules: str,
) -> Response[Any]:
    """Get very detailed information for a particular stock.

    The next portions of data can be retrieved with the service:
    `summaryDetail` `assetProfile` `fundProfile` `financialData` `defaultKeyStatistics` `calendarEvents`
    `incomeStatementHistory` `incomeStatementHistoryQuarterly` `cashflowStatementHistory`
    `balanceSheetHistory` `earnings` `earningsHistory` `insiderHolders` `cashflowStatementHistory`
    `cashflowStatementHistoryQuarterly` `insiderTransactions` `secFilings` `indexTrend` `sectorTrend`
    `earningsTrend` `netSharePurchaseActivity` `upgradeDowngradeHistory` `institutionOwnership`
    `recommendationTrend` `balanceSheetHistory` `balanceSheetHistoryQuarterly` `fundOwnership`
    `majorDirectHolders` `majorHoldersBreakdown`, `price`, `quoteType`, `esgScores`

    Args:
        symbol (str):  Example: AAPL.
        lang (Union[Unset, None, str]):  Example: en.
        region (Union[Unset, None, str]):  Example: US.
        modules (str):  Example: defaultKeyStatistics,assetProfile.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        symbol=symbol,
        client=client,
        lang=lang,
        region=region,
        modules=modules,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
