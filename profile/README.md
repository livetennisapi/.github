<div align="center">

<img src="https://raw.githubusercontent.com/livetennisapi/.github/main/profile/banner.jpg" alt="Live Tennis API" width="720">

**Real-time tennis data over REST and WebSocket.**
Live scores, players, rankings, match-winner market prices and model win-probability — for ATP, WTA, Challenger and ITF.

[**Documentation**](https://docs.livetennisapi.com) · [**Website**](https://livetennisapi.com) · [**Pricing**](https://livetennisapi.com/#pricing) · [**Get an API key**](https://livetennisapi.com/#pricing)

</div>

---

## SDKs

| | Install | |
|---|---|---|
| **Python** | `pip install livetennisapi` | [PyPI](https://pypi.org/project/livetennisapi/) · [source](https://github.com/livetennisapi/livetennisapi-python) |
| **JavaScript / TypeScript** | `npm install livetennisapi` | [npm](https://www.npmjs.com/package/livetennisapi) · [source](https://github.com/livetennisapi/livetennisapi-js) |
| **MCP server** | `npx livetennisapi-mcp` | [npm](https://www.npmjs.com/package/livetennisapi-mcp) · [source](https://github.com/livetennisapi/livetennisapi-mcp) |

```python
from livetennisapi import LiveTennisAPI

with LiveTennisAPI() as client:                       # reads LIVETENNISAPI_KEY
    for match in client.list_matches(status="live"):
        print(match.tournament, match.score.sets)
```

```ts
import { LiveTennisAPI } from 'livetennisapi';

const { data } = await new LiveTennisAPI().listMatches({ status: 'live' });
```

Both ship a `livetennis` CLI and a reconnecting WebSocket client. The MCP server
gives Claude, Cursor and other LLM agents 12 read-only tools over the same data.

## Quickstart (raw HTTP)

Every response is JSON. Authenticate with a bearer token or an `X-API-Key` header — either works.

```bash
curl https://api.livetennisapi.com/api/public/v1/matches?status=live \
  -H "Authorization: Bearer $LIVETENNISAPI_KEY"
```

```jsonc
{
  "data": [
    {
      "id": 18953,
      "tournament": "ATP Wimbledon",
      "surface": "grass",
      "round": "R16",
      "status": "live",
      "players": { "p1": { "name": "…", "ranking": 3 }, "p2": { "name": "…" } },
      "score": { "sets": [1, 1], "games": [[6, 3, 2], [4, 6, 1]], "points": ["40", "30"], "server": 1 }
    }
  ],
  "meta": { "limit": 50, "offset": 0, "count": 1 }
}
```

No key yet? The liveness probe needs no auth:

```bash
curl https://api.livetennisapi.com/api/public/v1/health
# {"status":"ok","version":"v1"}
```

## Endpoints

| Endpoint | Returns | Tier |
|---|---|:--:|
| `GET /matches` | Matches by lifecycle (`live` · `upcoming` · `completed`) | BASIC |
| `GET /matches/{id}` | Full match detail | BASIC |
| `GET /matches/{id}/score` | Current score only — lowest-latency read | BASIC |
| `GET /matches/{id}/events` | Match events, newest first | PRO |
| `GET /matches/{id}/analysis` | Model analysis — thesis + profile | ULTRA |
| `GET /players` | Search players by name | BASIC |
| `GET /players/{id}` | Bio, ranking, cached stats | BASIC |
| `GET /markets` | Match-winner market for a match | PRO |
| `GET /markets/{id}/prices` | Recent price ticks per side | PRO |
| `GET /history/matches` | Completed matches with derived winner | BASIC |
| `GET /fixtures` | Upcoming scheduled fixtures | BASIC |
| `GET /health` | Liveness probe (no auth) | — |
| `WS /ws` | Live score push feed | ULTRA |

## Tiers

| | BASIC | PRO | ULTRA |
|---|:--:|:--:|:--:|
| Matches, scores, players, fixtures, history | ✅ | ✅ | ✅ |
| Match events + market prices | — | ✅ | ✅ |
| Model analysis + `win_probability_p1` / `danger` | — | — | ✅ |
| WebSocket live feed | — | — | ✅ |
| Rate limit | 60/min · 10k/day | 300/min · 100k/day | 600/min · 500k/day |
| | $9.99/mo | $29.99/mo | $99.99/mo |

Calling above your tier returns `403 {"error":"upgrade_required"}` — never a silent empty result.

## Conventions

- **Base URL** — `https://api.livetennisapi.com/api/public/v1`
- **Timestamps** — UTC ISO 8601 with a `Z` suffix, everywhere.
- **Lists** return `{data, meta}`; single resources return the object directly.
- **Pagination** — `limit` (default 50, max 200) and `offset`.
- **Score shape** — `sets` is `[sets_p1, sets_p2]`; `games` is `[games_p1, games_p2]` where each side is a *per-set* list, so `[[6,3,2],[4,6,1]]` reads 6-4, 3-6, 2-1.
- **Forward compatibility** — ignore unknown fields. Additive changes land within `v1`, so clients should not reject responses carrying fields they don't recognise.
- **Errors** — `401 unauthorized` · `403 upgrade_required` · `404` · `429` (with `Retry-After`).

## Documentation

- **[docs.livetennisapi.com](https://docs.livetennisapi.com)** — interactive API reference
- **[Plain-HTML reference](https://docs.livetennisapi.com/reference.html)** — the same
  content with no JavaScript, readable by any client or crawler
- **[OpenAPI 3.1 specification](https://github.com/livetennisapi/openapi)** — generate a
  client in any language
- **[llms.txt](https://livetennisapi.com/llms.txt)** — a machine-readable summary for
  answer engines

## Where to subscribe

Direct is cheapest and issues a key instantly. The API is also listed on the
marketplaces you may already be billing through:

[Direct](https://livetennisapi.com/#pricing) ·
[RapidAPI](https://rapidapi.com/contact-whTqTESH5/api/tennis-data-analytics-api3) ·
[Apify](https://apify.com/livetennisapi/tennis-data-analytics) ·
[API.market](https://api.market/store/live-tennis-api/tennis-data-analytics) ·
[Zyla](https://zylalabs.com/api-marketplace/other/tennis+data+and+analytics+api/13207) ·
[Postman](https://www.postman.com/livetennisapi)

## Status

The API is live and serving. Anything published in this organisation is tested against the
production endpoint before release — see each repository's contract tests.

<div align="center">
<sub>Built by the team behind <a href="https://livetennisapi.com">livetennisapi.com</a></sub>
</div>
