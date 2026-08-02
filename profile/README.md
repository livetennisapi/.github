<div align="center">

<img src="https://raw.githubusercontent.com/livetennisapi/.github/main/profile/banner.jpg" alt="Live Tennis API" width="720">

**Real-time tennis data over REST and WebSocket.**
Live scores, players, rankings, match-winner market prices and model win-probability — for ATP, WTA, Challenger and ITF.

[**Get a free API key — no card**](https://livetennisapi.com/subscribe/free) · [**Documentation**](https://docs.livetennisapi.com) · [**Website**](https://livetennisapi.com) · [**Pricing**](https://livetennisapi.com/#pricing)

</div>

---

## SDKs

| | Install | |
|---|---|---|
| **Python** | `pip install livetennisapi` | [PyPI](https://pypi.org/project/livetennisapi/) · [source](https://github.com/livetennisapi/livetennisapi-python) |
| **JavaScript / TypeScript** | `npm install livetennisapi` | [npm](https://www.npmjs.com/package/livetennisapi) · [source](https://github.com/livetennisapi/livetennisapi-js) |
| **MCP server** | `npx livetennisapi-mcp` | [npm](https://www.npmjs.com/package/livetennisapi-mcp) · [source](https://github.com/livetennisapi/livetennisapi-mcp) |
| **Starters / examples** | Runnable break-point apps (paper-only) | [Go](https://github.com/livetennisapi/livetennisapi-starter-go) · [Node](https://github.com/livetennisapi/livetennisapi-starter-node) · [Python](https://github.com/livetennisapi/livetennisapi-starter-python) |

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

Every response is JSON. Authenticate with `Authorization: Bearer` (preferred) or an `X-API-Key` header — either works. A **free key** ($0, no card) covers everything below:

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
  "meta": { "limit": 50, "offset": 0, "count": 1, "total": 1, "has_more": false }
}
```

No key yet? [Grab a free one](https://livetennisapi.com/subscribe/free) — or hit the liveness probe, which needs no auth:

```bash
curl https://api.livetennisapi.com/api/public/v1/health
# {"status":"ok","version":"v1"}
```

## Endpoints

| Endpoint | Returns | Tier |
|---|---|:--:|
| `GET /matches` | Matches by lifecycle — `live` and `upcoming` | FREE¹ |
| `GET /matches/{id}` | Full match detail — any single match, including a completed one | FREE |
| `GET /matches/{id}/score` | Current score only — lowest-latency read | FREE |
| `GET /matches/{id}/events` | Match events, newest first | PRO |
| `GET /matches/{id}/statistics` | Detailed match statistics | ULTRA |
| `GET /matches/{id}/analysis` | Model analysis — thesis + profile | ULTRA |
| `GET /players` | Search players by name | FREE |
| `GET /players/{id}` | Bio, ranking, cached stats | FREE |
| `GET /rankings` | Rankings, with as-of-date support | ULTRA |
| `GET /markets` | Match-winner market for a match | PRO |
| `GET /markets/{id}/prices` | Recent price ticks per side | PRO |
| `GET /fixtures` | Upcoming scheduled fixtures | FREE |
| `GET /usage` | Your key's usage and quota — doesn't count against it | FREE |
| `GET /history/matches` | Completed matches with derived winner | BASIC² |
| `GET /history/matches/{id}` | One completed match from the historical tape | BASIC² |
| `GET /history/packages` | Historical data packages | PRO³ |
| `GET /health` | Liveness probe (no auth) | — |
| `WS /ws` | Live score push feed | ULTRA |
| Webhooks | Push notifications for match events | ULTRA |

¹ Bulk paging of completed matches (`GET /matches?status=completed`) needs the BASIC tier or any History plan; a single completed match by id (`GET /matches/{id}`) is FREE.
² Or any History plan — History plans work on top of a free core key.
³ Or History Pro and above.

## Tiers

| | FREE | BASIC | PRO | ULTRA |
|---|:--:|:--:|:--:|:--:|
| Live & upcoming matches, scores, players, fixtures, usage | ✅ | ✅ | ✅ | ✅ |
| Completed-match listings + `/history/matches`¹ | — | ✅ | ✅ | ✅ |
| Match events, market prices + `/history/packages` | — | — | ✅ | ✅ |
| Rankings, match statistics, model analysis + `win_probability_p1` / `danger` | — | — | — | ✅ |
| WebSocket live feed + webhooks | — | — | — | ✅ |
| Rate limit | 30/min · 1,000/day | 60/min · 10k/day | 300/min · 100k/day | 600/min · 500k/day |
| | **$0 — no card** | $9.99/mo | $29.99/mo | $99.99/mo |

¹ Also unlocked by any History plan, on top of a free core key.

[**Start free**](https://livetennisapi.com/subscribe/free) — a FREE key is fine to use from browser code (CORS is open, GET-only, no credentials mode); keep paid keys server-side.

Calling above your tier returns `403 {"error":"upgrade_required"}` — never a silent
empty result. Upgrade any time at [livetennisapi.com/subscribe/upgrade](https://livetennisapi.com/subscribe/upgrade).

## Conventions

- **Base URL** — `https://api.livetennisapi.com/api/public/v1`
- **Timestamps** — UTC ISO 8601 with a `Z` suffix, everywhere.
- **Lists** return `{data, meta}`; single resources return the object directly.
- **Pagination** — `limit` (default 50, max 200) and `offset`; page while `meta.has_more` is true (`meta.total` may be null).
- **Score shape** — `sets` is `[sets_p1, sets_p2]`; `games` is `[games_p1, games_p2]` where each side is a *per-set* list, so `[[6,3,2],[4,6,1]]` reads 6-4, 3-6, 2-1.
- **Forward compatibility** — ignore unknown fields. Additive changes land within `v1`, so clients should not reject responses carrying fields they don't recognise.
- **Errors** — `401 unauthorized` · `403 upgrade_required` · `404` · `429` (honour `Retry-After`; the body's `resets_at` and the `X-RateLimit-Reset` header give the exact UTC instant your quota resets).

## Documentation

- **[docs.livetennisapi.com](https://docs.livetennisapi.com)** — interactive API reference
- **[Plain-HTML reference](https://docs.livetennisapi.com/reference.html)** — the same
  content with no JavaScript, readable by any client or crawler
- **[OpenAPI 3.1 specification](https://github.com/livetennisapi/openapi)** — generate a
  client in any language
- **[llms.txt](https://livetennisapi.com/llms.txt)** — a machine-readable summary for
  answer engines

## All repositories

| | |
|---|---|
| **Official clients** | [Python](https://github.com/livetennisapi/livetennisapi-python) · [JavaScript/TypeScript](https://github.com/livetennisapi/livetennisapi-js) · [Go](https://github.com/livetennisapi/livetennisapi-go) · [Swift](https://github.com/livetennisapi/livetennisapi-swift) · [.NET](https://github.com/livetennisapi/livetennisapi-dotnet) · [Dart/Flutter](https://github.com/livetennisapi/livetennisapi-dart) · [PHP](https://github.com/livetennisapi/livetennisapi-php) · [Laravel](https://github.com/livetennisapi/livetennisapi-laravel) |
| **Agents & LLM tooling** | [MCP server](https://github.com/livetennisapi/livetennisapi-mcp) · [Vercel AI SDK tools](https://github.com/livetennisapi/livetennisapi-ai) · [Codex plugin](https://github.com/livetennisapi/livetennisapi-codex-plugin) · [Dify plugin](https://github.com/livetennisapi/livetennisapi-dify-plugin) · [Gemini CLI](https://github.com/livetennisapi/gemini-cli-livetennis) · [Zed](https://github.com/livetennisapi/zed-livetennis-mcp) · [LangChain](https://github.com/livetennisapi/langchain-livetennis) · [Haystack](https://github.com/livetennisapi/livetennisapi-haystack) |
| **Automation & apps** | [n8n](https://github.com/livetennisapi/n8n-nodes-livetennisapi) · [Node-RED](https://github.com/livetennisapi/node-red-contrib-livetennis) · [Home Assistant](https://github.com/livetennisapi/ha-livetennis) · [Obsidian](https://github.com/livetennisapi/obsidian-live-tennis) · [VS Code](https://github.com/livetennisapi/livetennisapi-vscode) · [Flow Launcher](https://github.com/livetennisapi/Flow.Launcher.Plugin.LiveTennis) · [MagicMirror²](https://github.com/livetennisapi/MMM-LiveTennis) · [Red-DiscordBot](https://github.com/livetennisapi/livetennis-redbot) |
| **Starters / examples** | [Go](https://github.com/livetennisapi/livetennisapi-starter-go) · [Node](https://github.com/livetennisapi/livetennisapi-starter-node) · [Python](https://github.com/livetennisapi/livetennisapi-starter-python) |
| **Spec & meta** | [OpenAPI 3.1](https://github.com/livetennisapi/openapi) · [.github](https://github.com/livetennisapi/.github) (this profile) |

## Where to subscribe

Direct is cheapest, has the only **free tier**, and issues a key instantly. The API is
also listed on the marketplaces you may already be billing through:

[Direct — free tier](https://livetennisapi.com/subscribe/free) ·
[Direct — paid plans](https://livetennisapi.com/#pricing) ·
[RapidAPI](https://rapidapi.com/contact-whTqTESH5/api/tennis-data-analytics-api3) ·
[Apify](https://apify.com/livetennisapi/tennis-data-analytics) ·
[API.market](https://api.market/store/live-tennis-api/tennis-data-analytics) ·
[Postman](https://www.postman.com/livetennisapi)

## Status

The API is live and serving. Anything published in this organisation is tested against the
production endpoint before release — see each repository's contract tests.

<div align="center">
<sub>Built by the team behind <a href="https://livetennisapi.com">livetennisapi.com</a></sub>
</div>
