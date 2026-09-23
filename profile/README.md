<a href="https://livetennisapi.com/">
  <picture>
    <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/livetennisapi/.github/main/profile/assets/hero-mobile.svg">
    <img src="https://raw.githubusercontent.com/livetennisapi/.github/main/profile/assets/hero.svg" alt="From the court. Into your code. A tennis ball connects to branching data paths." width="1280">
  </picture>
</a>

# Live Tennis API

Live tennis scores and historical data for apps, dashboards and research.
Coverage includes ATP, WTA, Challenger, ITF and junior Grand Slam draws. Available fields vary by match and tour.

[**Get a free API key**](https://livetennisapi.com/subscribe/free) &nbsp; / &nbsp; [Documentation](https://docs.livetennisapi.com/) &nbsp; / &nbsp; [Plans](https://livetennisapi.com/#pricing) &nbsp; / &nbsp; [Developer portal](https://livetennisapi.com/account)

## Make your first request

Set `LIVETENNISAPI_KEY` in your environment, then fetch the matches in play.

```bash
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer $LIVETENNISAPI_KEY" \
  "https://api.livetennisapi.com/api/public/v1/matches?status=live"
```

Free includes live scores, players and fixtures at 30 requests/minute and 100/day. No card required. Keep paid keys server-side.

## Pick your starting point

- [Python client](https://github.com/livetennisapi/livetennisapi-python). Install with `pip install livetennisapi`. [PyPI package](https://pypi.org/project/livetennisapi/).
- [JavaScript and TypeScript client](https://github.com/livetennisapi/livetennisapi-js). Install with `npm install livetennisapi`. [npm package](https://www.npmjs.com/package/livetennisapi).
- [MCP server](https://github.com/livetennisapi/livetennisapi-mcp). Connect an AI client with `npx livetennisapi-mcp`. [npm package](https://www.npmjs.com/package/livetennisapi-mcp).
- [OpenAPI 3.1 specification](https://github.com/livetennisapi/openapi). Generate a client for your stack or inspect the request and response schemas.

The Python and JavaScript clients include a `livetennis` CLI and a reconnecting WebSocket client. Streaming requires Ultra.

<details>
<summary>Python and JavaScript examples</summary>

Both clients read `LIVETENNISAPI_KEY` from the environment.

```python
from livetennisapi import LiveTennisAPI

with LiveTennisAPI() as client:
    for match in client.list_matches(status="live"):
        print(match.tournament, match.score.sets)
```

```ts
import { LiveTennisAPI } from 'livetennisapi';

const client = new LiveTennisAPI();
const { data } = await client.listMatches({ status: 'live' });
console.log(data);
```

Prefer raw HTTP? The API also accepts `X-API-Key` authentication.
Check connectivity without a key at [`GET /health`](https://api.livetennisapi.com/api/public/v1/health).

</details>

## Choose your data

- Free covers live and upcoming matches, current scores, players, fixtures and the tournament catalogue.
- Basic adds completed-match history, point-by-point tapes where available, the 1968-2022 results archive and head-to-head records.
- Pro adds match events, market prices, ranking tables and monthly history packages.
- Ultra adds live model fields, match statistics, shot-level charting and streaming. It also includes as-of rankings and webhooks.

Each plan includes the plans below it. [Compare current plans](https://livetennisapi.com/#pricing) or [upgrade an existing key](https://livetennisapi.com/subscribe/upgrade).
The [Historical Data API](https://livetennisapi.com/historical-tennis-data-api) also has standalone plans.

Results, point-by-point records and shot-level charting have different coverage. Check the [API reference](https://docs.livetennisapi.com/reference.html) before choosing data for your project.

<details>
<summary>Endpoint guide and access rules</summary>

The base URL is `https://api.livetennisapi.com/api/public/v1`.
This guide covers the main routes. The [full reference](https://docs.livetennisapi.com/reference.html) includes parameters and plan exceptions.

| Route | Data |
| --- | --- |
| `GET /matches` | Live, upcoming or completed matches |
| `GET /matches/{id}` | One match |
| `GET /matches/{id}/score` | Current score |
| `GET /matches/{id}/events` | Match events |
| `GET /matches/{id}/points` | Recorded live points where covered |
| `GET /matches/{id}/prices` | Match market prices |
| `GET /matches/{id}/statistics` | Match statistics |
| `GET /matches/{id}/analysis` | Model analysis |
| `GET /players` and `GET /players/{id}` | Player search and profiles |
| `GET /h2h` | Head-to-head records |
| `GET /rankings` | Ranking listings or a player's as-of record |
| `GET /markets` and `GET /markets/{id}/prices` | Match-winner markets and prices |
| `GET /fixtures` | Scheduled fixtures |
| `GET /tournaments` | Tournament catalogue |
| `GET /usage` | Your quota and usage |
| `GET /history/matches` | Completed-match listings |
| `GET /history/matches/{id}` | A match's point-by-point tape |
| `GET /history/coverage` | Measured historical coverage |
| `GET /history/archive/...` | The 1968-2022 results archive |
| `GET /history/matches/{id}/rally` and `GET /rally/matches` | Shot-by-shot charted data |
| `GET /charting/...` | Match and player charting statistics |
| `GET /history/packages` | Historical downloads |
| `GET /health` | Liveness check without authentication |
| `WS /ws` and `GET /ws-token` | Live score feeds |
| Webhooks | Match event notifications |

Completed-match listings require Basic or a History plan. A single completed match at `/matches/{id}` is available on Free.
Free also includes a limited monthly history sample. See the [current access rules](https://docs.livetennisapi.com/reference.html#plans) for its limits.

The results archive spans 1968-2022. Reconstructed archive tapes cover some matches from 2013-2022, with null timestamps and no model probabilities.
Those tapes require Ultra or an active History plan. Bulk download rules differ from single-match access.

Historical tapes from 2023 onward declare their coverage and source. Model outputs appear only where computed.
Shot-level data is curated and does not cover every match.

Calling above your plan returns `403 upgrade_required`.
The reference documents the data fields and exceptions for each route.

</details>

<details>
<summary>Response conventions</summary>

- Lists return `{data, meta}`. Single-resource reads return the resource.
- Timestamps use UTC ISO 8601 with a `Z` suffix where a real timestamp exists.
- Page with `limit` and `offset`. Continue while `meta.has_more` is true. The default limit is 50 and the maximum is 200.
- Scores use player-major arrays. `games: [[6, 3, 2], [4, 6, 1]]` means 6-4, 3-6, 2-1.
- Ignore unknown fields so additive changes in `v1` do not break your client.
- Handle `401`, `403`, `404` and `429` responses. Follow `Retry-After` when rate limited.

</details>

## Build with Synapse

[Synapse](https://synapsereality.io/) builds custom software, AI integrations and automations.
Have a product in mind? [Talk to Synapse](https://synapsereality.io/contact/) about building it.

## More ways to build

<details>
<summary>Client libraries, integrations and example apps</summary>

### Client libraries

[Python](https://github.com/livetennisapi/livetennisapi-python),
[JavaScript and TypeScript](https://github.com/livetennisapi/livetennisapi-js),
[Go](https://github.com/livetennisapi/livetennisapi-go),
[Swift](https://github.com/livetennisapi/livetennisapi-swift),
[.NET](https://github.com/livetennisapi/livetennisapi-dotnet),
[Dart and Flutter](https://github.com/livetennisapi/livetennisapi-dart),
[PHP](https://github.com/livetennisapi/livetennisapi-php),
[Laravel](https://github.com/livetennisapi/livetennisapi-laravel).

### AI tools

[MCP server](https://github.com/livetennisapi/livetennisapi-mcp),
[Vercel AI SDK](https://github.com/livetennisapi/livetennisapi-ai),
[Codex plugin](https://github.com/livetennisapi/livetennisapi-codex-plugin),
[Dify](https://github.com/livetennisapi/livetennisapi-dify-plugin),
[Gemini CLI](https://github.com/livetennisapi/gemini-cli-livetennis),
[Zed](https://github.com/livetennisapi/zed-livetennis-mcp),
[LangChain](https://github.com/livetennisapi/langchain-livetennis),
[Haystack](https://github.com/livetennisapi/livetennisapi-haystack).

### Automation and apps

[n8n](https://github.com/livetennisapi/n8n-nodes-livetennisapi),
[Node-RED](https://github.com/livetennisapi/node-red-contrib-livetennis),
[Home Assistant](https://github.com/livetennisapi/ha-livetennis),
[Obsidian](https://github.com/livetennisapi/obsidian-live-tennis),
[VS Code](https://github.com/livetennisapi/livetennisapi-vscode),
[Flow Launcher](https://github.com/livetennisapi/Flow.Launcher.Plugin.LiveTennis),
[MagicMirror](https://github.com/livetennisapi/MMM-LiveTennis),
[Red-DiscordBot](https://github.com/livetennisapi/livetennis-redbot).

### Example apps and research

The [Go](https://github.com/livetennisapi/livetennisapi-starter-go),
[Node](https://github.com/livetennisapi/livetennisapi-starter-node) and
[Python](https://github.com/livetennisapi/livetennisapi-starter-python) starters demonstrate break-point apps with paper orders only.

The [Polymarket tennis toolkit](https://github.com/livetennisapi/polymarket-tennis) compares tennis market prices with live match state. It is observe-only.
The [academic dataset](https://github.com/livetennisapi/livetennisapi-data) includes research access details and data loaders.

[Browse all repositories](https://github.com/orgs/livetennisapi/repositories).

</details>

<details>
<summary>Documentation, marketplaces and partners</summary>

### Documentation

[Interactive API reference](https://docs.livetennisapi.com/),
[plain HTML reference](https://docs.livetennisapi.com/reference.html),
[OpenAPI specification](https://github.com/livetennisapi/openapi),
[llms.txt](https://livetennisapi.com/llms.txt).

### Marketplaces

Subscribe [directly](https://livetennisapi.com/#pricing) or through
[RapidAPI](https://rapidapi.com/contact-whTqTESH5/api/tennis-data-analytics-api3),
[Apify](https://apify.com/livetennisapi/tennis-data-analytics) or
[API.market](https://api.market/store/live-tennis-api/tennis-data-analytics).
Explore requests in the [Postman workspace](https://www.postman.com/livetennisapi).

### Partners

Refer developers through the [affiliate program](https://affiliates.livetennisapi.com/program).
The program page has the current terms and commission details.

</details>

---

[livetennisapi.com](https://livetennisapi.com/) &nbsp; / &nbsp; [hello@livetennisapi.com](mailto:hello@livetennisapi.com) &nbsp; / &nbsp; [Report a security issue](https://github.com/livetennisapi/.github/blob/main/SECURITY.md)
