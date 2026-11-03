# Pass B: what the owner does before stage A

Written 20261103 01:20 UTC. It belongs to [the pass-B plan](pass-b-plan.md); that page says why, this one says how. Nothing here
spends money. **Nothing paid starts until you have answered the five decisions below and given an explicit yes with model, provider
and cap (D-14).** The commands are for **your own terminal**, so that the key never passes through the conversation (D-20).

## 1. Five answers I need

Decisions 1 and 2 are made (D-30: OpenAI `gpt-6-luna`, reasoning off, USD 3 in all). A one-line reply is enough, for example
"3 yes, 4 local, 5 all four, 6 done, 7 two".

| # | Question | My recommendation | If you disagree |
|---|---|---|---|
| 3 | May the 20 article texts go to OpenAI's API? | Yes (the text is never committed) | No: the pilot stops here and nothing more is run |
| 4 | Embeddings | Local `qwen3-embedding:0.6b`, free, as in pass A | OpenAI `text-embedding-3-small`, about USD 0.002 more and a second price to track |
| 5 | Builders | All four, in the order LightRAG, fast-graphrag, Microsoft GraphRAG, nano-graphrag | A subset, named |
| 6 | Key and hard limit | Sections 2 and 3 below, then "done" and the key file's path (never its content) | Say that no provider-side limit exists and the gateway is the only guard (I advise against it) |
| 7 | How many yeses | Two: stages A to C, then D with C's numbers in hand | One for everything |

## 2. At OpenAI: a project of its own, a hard limit, a restricted key

The reason for a separate project: a project's hard limit "applies only to API traffic billed to that project", so the limit
covers the pilot and nothing else, and deleting the project afterwards removes both. What I have from OpenAI's pages, with how I got
it:

- **Spend limit (read directly, 20261103, before 01:16 UTC,
  [Spend limits](https://developers.openai.com/api/docs/guides/spend-limits)).** Path given there: project settings, **Limits**,
  **Spend**, **Edit spend limit**, enter the **Monthly spend limit**, turn on **Enforce a hard limit**, **Save**. Without that switch
  the limit does not stop requests: "Spend alerts do not enforce a cap." At the limit, requests return a `429` with
  `project_spend_limit_exceeded`. "Enforcement is not instantaneous, so recorded spend can slightly exceed the configured amount";
  the page gives no figure.
- **Key (search summary only, 20261103, before 01:16 UTC).** The help article on projects returned HTTP 403 to me, so the key steps below
  are a search engine's summary of it, not the page: open the project, **API Keys**, **+ Create new secret key**, with permissions
  **Restricted** and per-resource levels. The page on roles ([Manage permissions](https://developers.openai.com/api/docs/guides/rbac),
  read directly) lists **Model capabilities** (`api.model.request`) as "Make requests to chat completions, audio, embeddings, and
  images". The pilot needs only chat completions, so give the key that one permission at **Request** and nothing else. The labels
  on your screen may differ from these; if they do, send me what you see.
- **Expiry.** OpenAI "strongly recommend[s] setting an expiration date when you create a project API key"
  ([Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices), read directly). Choose a
  few days.

Do this, in order:

1. Create a project for the pilot only (its name is yours; mine would be `kb-kg-pilot`).
2. In that project: **Limits**, **Spend**, monthly limit **USD 3**, **Enforce a hard limit** on. Optionally add an alert at USD 2;
   an alert only notifies.
3. In that project: create a key, restricted to **Model capabilities: Request**, with an expiry of a few days. Copy it once; the
   dialog may not show it again.
4. If your account bills from a prepaid balance, a balance of USD 3 to 5 is a second limit: an empty balance returns
   `credit_balance_exhausted`. Whether your account is prepaid, and your usage tier and rate limits, are **unstated** to me.

## 3. Put the key in a file only you can read (D-20)

Run this in your own zsh terminal (not in a tab I opened). It asks for the key without echoing it, writes it to a mode-600 file in
a directory only you can enter, outside every repository and outside the session's scratch directory, and prints no key. Change
the directory name if you like; tell me the path afterwards.

```bash
mkdir -p -m 700 ~/.config/kb-kg-pilot
umask 077
read -rs "KEY?Paste the OpenAI key, then press Return: "; echo
printf '%s\n' "$KEY" > ~/.config/kb-kg-pilot/openai.key
unset KEY
chmod 600 ~/.config/kb-kg-pilot/openai.key
```

Check it without printing it:

```bash
ls -l ~/.config/kb-kg-pilot/openai.key
```

```bash
grep -c '^sk-' ~/.config/kb-kg-pilot/openai.key
```

The first command should show `-rw-------`; the second should print `1` (OpenAI keys begin `sk-`; if yours does not, tell me, and
do not paste it). The gateway refuses a key file
that group or others can read, that holds more than one line, or that is longer than 4 KiB, and it never prints the key. I never
open the file; the gateway process reads it when a stage starts. A key that was typed or pasted twice is refused by the gateway's own
shape check.

## 4. What I do after your answers

| Step | What happens | Money |
|---|---|---|
| Write the stage profile | The prices are read again from OpenAI's pricing page and stamped with the read time; the profile names the key file, the ledger directory and the cap | None |
| Dry runs | `passb_stage_a.py extract`, then `run` without `--send`, then `passb_stage.py` without `--send`: each prints the plan and the worst case and starts nothing | None |
| Stage A, with your yes | At most 12 calls and USD 0.10; then a refusal test with a tiny cap. You compare OpenAI's usage page with the gateway's total by hand | At most USD 0.10 |
| Stages B and C | One yes covers A to C when you give one (decision 7, option "two") | About USD 0.3 at the central estimate, at most 0.9 by the limits |
| Stage D | Its own yes, with C's numbers shown first | About USD 0.6, at most 1.5 |

## 5. Afterwards

Delete the key file (`rm ~/.config/kb-kg-pilot/openai.key`), revoke the key in the project's **API Keys** page, and delete the
project or lower its limit to zero. Nothing about the key is in this repository.

## What I could not check

OpenAI's help articles on projects and key permissions (HTTP 403 to my fetcher), so the key-creation labels are second-hand; whether
your account has a project limit available, is prepaid, or has a usage tier that limits `gpt-6-luna`; and how much spend can slip
past a hard limit while "the limit state propagates". The third is why the gateway's cap and the provider's limit are both kept:
neither is a guarantee on its own.
