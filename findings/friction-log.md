# Friction log: first-time setup and use of Native (public snapshot)

Snapshot tested: `withnative/native` @ `c4edccfba9c93deebf417b20e0db4a409cb1a828` (shallow clone, 19 Nov 2026)
Machine: macOS (Apple Silicon, 12 cores, 24 GB RAM), OpenCode 1.18.3

Each entry: what happened → why it matters → suggested fix.

## Discovery and docs

1. **Two "Native"s.** Searching "withnative" lands on withnative.com, an unrelated enterprise AI consultancy. The HN job post and X bio use withnative.ai.
   → Candidates and users can end up on the wrong company.
   → Fix: say "withnative.ai" in full every time it's written, and claim the obvious X/LinkedIn handles.

2. **Benchmark headline numbers don't quite agree with each other.** The post's summary says "97% fewer failed trials" while the body says "30× fewer"; the chart says 43.5× while the headline says 40×.
   → Sharp readers will pick at it, and it distracts from a strong result.
   → Fix: one table of exact numbers, with headlines that round down from it.

3. **The Stanford link is in the HN post, but not in the benchmark post.** The homepage says the product is "based on research at Stanford University". The benchmark post has only Richard as the byline and no affiliation.
   → Fix: link the Stanford work directly from the benchmark post, or drop the claim near the benchmark.

## Install and build

5. **Build is quick and clean (good).** `cargo build --locked --bin mcp-stdio --bin native` took 3 min 04 s with debug info off. It used 2.4 GB for `target/` plus 1.8 GB for the Rust 1.98 toolchain, and printed one future-incompat warning (`proc-macro-error2`).
   → Worth saying in SELF_HOSTING.md: "about 3 minutes, about 4 GB disk".

6. **SELF_HOSTING.md says to call the `engine_info` tool, but no such tool is listed.** The default surface lists 10 executor tools. Calling `engine_info` the obvious way fails with `missing required string field 'operation'`; it's actually `system_read {operation: "engine_info"}`.
   → The very first check in the setup guide fails for a literal-minded agent.
   → Fix: update the verification step to the executor form, or keep `engine_info` as a direct alias.

## Agent experience over MCP

7. **Fixed context cost before the first useful call is about 16k tokens.** Tool definitions are about 23.6k characters (about 5.9k tokens), and the `bootstrap` JSON is about 42.5k characters (about 10.6k tokens; the text format is about 27k characters).
   → On small workspaces this can cost more than grepping a few files. A published "break-even workspace size" would make the 40× claim more credible.
   → Fix: a slim bootstrap mode for read-only question answering.

8. **The "why" field has three names and the rules differ.** `create_record` requires `reason`. `manage_links.add` rejects `reason` and takes `note`. `manage_relationships.assert` takes `rationale` and also requires `idempotency_key`, which is optional elsewhere.
   → Each mismatch costs an agent one failed round trip.
   → Fix: accept `reason` everywhere as an alias.

9. **The repair envelopes are excellent (keep them).** A failed call names the failing JSON pointer, the accepted and required fields, and for routing errors a ready-to-send `next_call`. Every mistake above cost exactly one retry, never a dead end.

10. **Most read operations fail on the first try.** `records_read` lists only `get_record` and `search` directly. `get_history`, `whats_changed`, `scan` and the rest must go through `call_executor`, so a natural first attempt is refused, though the repair fixes it in one call.
    → Fix: accept any `records_read` operation on the direct tool, even if only two are listed.

11. **Misleading "not authorized" on a valid query.** `SELECT count(*) AS n FROM catalog_operations` returns `query_sql [unauthorized_relation]: not authorized`, while `SELECT executor, operation FROM catalog_operations WHERE …` works.
    → Looks like an aggregate-detection quirk, and the error sends the agent in the wrong direction.

12. **There's no MCP guide for authoring artifacts.** `read_guide` has 37 topics. `rendered-artifacts` is about reading a displayed artifact, not making one. The authoring steps live in `docs/artifact-runtimes.md` (59 KB), which an MCP-only agent can't reach.

13. **The README's suggested first task stalls at "build an artifact that reads them".** The decision, the task, the `depends_on` link and the history all worked. The artifact did not after 7 calls:
    - `manage_artifact_inputs.bind` says "target must be a governed Collection", but neither the docs example ("Suppose a governed Collection…") nor the error says which Collection kinds qualify or how to make one.
    - `batch_write` takes `items`, not `writes`.
    - Each grant is plan-gated (prepare, then execute), so each costs two calls.
    → This is the "wow" step of the README, and it's the hardest one.
    → Fix: a `read_guide` topic `artifact-authoring` with the exact call sequence, or one convenience operation that binds a set of records or a SQL query to a new artifact and issues its grants.

## From the benchmark traces (443 agent trials over OpenCode)

14. **29% of searches came back empty because of `scope`.** 98 of 333 `records_read.search` calls had no results. Every one passed `scope` with a value like `"all"` or `"workspace"`, for plain queries like "Twilio" and "pricing" that do match. `scope` is a record ID (subtree), so Native returns `search: record all does not exist`. OpenCode shows that error to the model as an empty string, so the agent concludes "no results" and burns more calls.
    → Fix: treat `all` / `workspace` / `*` as "no scope", or rename the field to `subtree_id`. Short of that, say "record id" in the one-line tool description, since agents never read `describe_operation` first.

15. **Payloads are about 9× bigger than the Markdown they replace.** Median `get_record` result: 8.2k characters, against 0.9k for the agent reading the same note as a `.md` file. Median `search`: 4.1k characters (p90 20k). That, not the number of calls, is why strong models spent 2–3× more tokens with Native on the small corpus.
    → Fix: a `fields` / `compact` option on `get_record` and `search` (name, body, typed links, and the supersedes chain), and a smaller default.

16. **`bootstrap` is the single biggest fixed cost.** 91 of 140 Native trials called it, many as the very first call, and it returned about 41.6k characters every time. For a read-only question that's more than the whole Markdown trial used for strong models.
    → Fix: a slim bootstrap (`profile: "answer"`) of about 2k characters for read-only Q&A, with the full orientation one call away.

## Import

4. **Markdown import does not apply supersession.** `native import` reports up to 15 "supersession candidates (not applied, confirm with native init)". Typed `supersedes` links are what makes the benchmark's freshness questions cheap, so a user who only runs `import` gets less than the benchmark shows.
   → Fix: an `--apply-explicit-supersedes` option for candidates whose text says "replaces [[X]]" (explicit + high confidence), or a one-line next step printed after import.
