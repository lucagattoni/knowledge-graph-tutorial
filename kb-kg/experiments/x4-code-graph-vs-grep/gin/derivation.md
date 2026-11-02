# X4, gin: how the ten questions and their answers were derived

**Status: frozen before any agent or code-graph tool was run.** The questions and answers are in
[`questions.yaml`](questions.yaml). Nothing here is a result about a tool; it is the answer key and the evidence that the
key is right, with its limits.

## The repository, as read

| Item | Value | Source, read (UTC) |
|---|---|---|
| Repository | https://github.com/gin-gonic/gin, Go | fixed by the task |
| Pinned commit | `0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646` (default branch `master`) | `git fetch --depth 1 origin <hash>` then `git rev-parse HEAD` printed the same hash, 20261102 10:27 and again on a second fresh copy at 20261102 10:37 |
| Commit date | 2026-10-10T12:20:35+08:00, which is 2026-10-10T04:20:35Z; subject "docs: include HTTP QUERY method in RouterGroup.Any (#4879)" | `git log -1 --format=%H%n%cI%n%s`, 20261102 10:41 |
| Licence | **MIT**, "Copyright (c) 2014-present Manuel Martínez-Almeida"; the file is identical in both copies, SHA-256 `b104efb2c7700691650f27034e8541c5ae0ed9af54d884287f19a7467ca2fe7f` | `LICENSE` at the pinned commit, first lines read 20261102 10:27 |
| Size | 59 non-test `.go` files tracked (one is generated, `testdata/protoexample/test.pb.go`, which no question touches); 7 packages type-check with 0 errors; 483 function and method declarations | `git ls-files`; the type-checking tool, 20261102 10:30 |
| Module requirement | `go 1.26.0` in `go.mod` | read 20261102 10:27 |

## Tools and where they came from

| Tool | Version | Source, check, read (UTC) |
|---|---|---|
| Go toolchain | go1.27.3 darwin/arm64 (latest stable in the list) | Archive `go1.27.3.darwin-arm64.tar.gz` from `https://go.dev/dl/`. The published SHA-256 `dd3908cf20959d798c1e06ebe5b72213f0505ce01373b40ce3110975a6cd99c2` was read from `https://go.dev/dl/?mode=json` and also found in the HTML page `https://go.dev/dl/`; `shasum -a 256` of the downloaded file printed the same value. 20261102 10:27 |
| `golang.org/x/tools` | v0.52.0 (pulled by `go get ...@latest`) | module proxy, 20261102 10:28; used as a library by the Method 2 tool |
| `gopls` | v0.24.0 | `go install golang.org/x/tools/gopls@latest`, built 20261102 10:35; used for Method 3 |
| ripgrep | 14.1.1 (the copy built into the Claude Code CLI) | `rg --version`, 20261102 10:42 |

Gin's own dependencies (validator, sonic, quic-go and the rest of `go.mod`) were downloaded through the default module
proxy and checksum database and were type-checked, never executed. Every Go command ran under
`env -i PATH=<toolchain>:/usr/bin:/bin HOME=<scratch>/home GOTOOLCHAIN=local ...`, so no credential or personal variable
reached it. The toolchain, the clones and all helper scripts live in a scratch directory (`$SCRATCH/x4-gin/`), not in this
repository.

**No code-graph tool and no knowledge-graph tool was used to derive any answer** (in particular not codebase-memory-mcp,
the tool a later step tests).

## The three methods

All three read the same pinned commit. For every question the answer is what the methods agree on.

1. **Method 1: ripgrep and reading.** For each question I ran a plain search for the bare name over the non-test Go
   source (`rg -n --glob '*.go' --glob '!*_test.go' -e '\bNAME\b' .`) and read every hit together with the `func` line above
   it. From that reading I wrote one fixed textual rule per question, for example "a line matching `\bgroup\.handle\(`;
   its caller is the nearest `func` line above it". The rules are in `spec.py`; the program applies them and also lists
   every bare-name hit the rule did *not* take, so each skipped hit can be read and classified (the classifications are in the
   notes below). This method uses no parser and no type information, only text and my reading of receivers.
2. **Method 2: `go/types`.** A small program (`$SCRATCH/x4-gin/tool/main.go`, 271 lines, built on
   `golang.org/x/tools/go/packages`) loads the seven packages of the module without tests, type-checks them from source, and
   walks every identifier. A use that resolves to a function or method declared in this module becomes one record: callee,
   enclosing top-level declaration, file, line, and a kind (`call` when it is the function part of a call expression,
   `iface-call` when the callee is an interface method, `ref` for any other use such as a method value). It also records
   whether the use sits inside a function literal. The same program with `-defs` prints every declaration with its `func`
   line, doc-comment line and closing line. Result of the run on the pinned commit: 635 records (605 `call`, 29 `iface-call`,
   1 `ref`); 48 of them are inside function literals. No answer below involves a function literal.
3. **Method 3: `gopls`.** `gopls references file:line:col` on the declaration of each target (callers) and
   `gopls definition file:line:col` on a call site (definitions), then each reference location is mapped to its enclosing
   declaration. This is stock tooling, so anyone can repeat it (positions are in the last section).

**What is and is not independent.** Method 1 shares nothing with the other two (no parser, no type checker). Methods 2 and 3
both rest on `go/types`, so a type-checker error would reach both; I did not look for one. Method 3 is a separate program from
Method 2, so a bug in my walker would not reach it. I also saw Method 2's table of callee counts when I *chose* targets (I picked
callees with the right number of callers), so the choice of targets was informed by it; the answers themselves were then
computed independently by Methods 1 and 3 and compared.

Commands, from `$SCRATCH/x4-gin/` (the harness reads a checkout and writes `m1.json`, `m2.json`, `m3.json`):

```
git init -q gin && cd gin && git remote add origin https://github.com/gin-gonic/gin.git
git fetch --depth 1 origin 0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646 && git checkout -q FETCH_HEAD   # then: git rev-parse HEAD
python3 -I harness/derive.py gin out_main          # all three methods, ten questions
python3 -I harness/unmatched.py gin-recheck        # bare-name hits the Method 1 rules did not take
bin/cs -dir gin > run1.jsonl ; bin/cs -dir gin -defs > defs1.jsonl     # Method 2 on its own
```

SHA-256 of the helper sources (so a later run can tell whether they changed): `tool/main.go`
`9332cf09d2d867e3f95ea25529e26d40de70b80324dd0664228ba681c097b4a7`, `harness/spec.py`
`e12be09ce953ad9f54e484caf7688b2bd02616645cdc501c1e2c3c21e57d186f`, `harness/derive.py`
`55ecdd3d8c2ebfa506fa91cb7b2631c44585fa6960173ab1c7dc11a6e1aae115`, `harness/common.py`
`bd8c4ed15e5b8517bcf3c89495ae554a4398f28cfbb7478328038e043884a3f2`. These files are not committed to the repository.

## The ten questions

The first three are the pilot's, chosen by position and never by result. Counts below are of the key.

| # | id | Kind | Target | Key |
|---|---|---|---|---|
| 1 (pilot) | gin-01 | definition | method `Engine.handleHTTPRequest` | `gin.go:719` |
| 2 (pilot) | gin-02 | callers, at most 5 | `Context.hasRequestContext` | 4 callers |
| 3 (pilot) | gin-03 | callers, 6 to 15 | `RouterGroup.handle` | 11 callers |
| 4 | gin-04 | callers, shared name | `Context.Get` | 4 callers |
| 5 | gin-05 | definition, shared name | `Engine.Handler` | `gin.go:257` |
| 6 | gin-06 | callers in one file, self call | `setWithProperType` in `binding/form_mapping.go` | 3 callers |
| 7 | gin-07 | callers, concrete receiver only | `responseWriter.WriteHeaderNow` | 6 callers |
| 8 | gin-08 | definition, doc comment above | `node.getValue` | `tree.go:418` |
| 9 | gin-09 | callers, promoted method and a function variable | `RouterGroup.GET` | 3 callers |
| 10 | gin-10 | callers in one file, shared name | `Context.Error` in `context.go` | 2 callers |

Three are definitions and seven are callers; two of the callers questions (gin-06, gin-10) are the "which functions in file F
call G" kind. Questions whose answer a single grep does not give: gin-03, gin-04, gin-07, gin-09, gin-10 (and gin-05 needs the
receiver to separate two methods of the same name).

## Per-question evidence

In each table "key" is the answer in `questions.yaml`. "Agree" means the method's set (or location) equals the key.

### gin-01 (pilot), definition: `Engine.handleHTTPRequest`
| Method | Result | Agree |
|---|---|---|
| 1 | `rg '^func \(\w+ \*?Engine\) handleHTTPRequest\('` gives one hit, `gin.go:719` | yes |
| 2 | `go/ast` declaration: `gin.go` line 719, closes at line 789, no doc comment | yes |
| 3 | `gopls definition gin.go:701:9` (the call in `Engine.ServeHTTP`) answers `gin.go:719` | yes |

Resolution: none needed. The bare-name search lists two call sites (`gin.go:701`, `gin.go:713`) before the definition.

### gin-02 (pilot), callers: `Context.hasRequestContext`
Key: `context.go::Context.Deadline`, `context.go::Context.Done`, `context.go::Context.Err`, `context.go::Context.Value`.

| Method | Result | Agree |
|---|---|---|
| 1 | rule `\bc\.hasRequestContext\(\)`: 4 callers (lines 1502, 1510, 1518, 1539) | yes |
| 2 | 4 `call` records at the same lines, none in a function literal, no `ref` | yes |
| 3 | `gopls references context.go:1494:19`: the same 4 outside tests | yes |

Skipped bare-name hits, read and classified: the declaration (1494), a local variable of the same name declared at 1496
and read at 1497 inside the method itself, and a comment (1493). None is a call.

### gin-03 (pilot), callers: `RouterGroup.handle`
Key: `routergroup.go::RouterGroup.` plus `Any`, `DELETE`, `GET`, `HEAD`, `Handle`, `Match`, `OPTIONS`, `PATCH`, `POST`,
`PUT`, `QUERY` (11 names).

| Method | Result | Agree |
|---|---|---|
| 1 | rule `\bgroup\.handle\(`: 11 callers (lines 133 to 193) | yes |
| 2 | 11 `call` records, none in a function literal | yes |
| 3 | `gopls references routergroup.go:110:27`: the same 11 outside tests | yes |

Skipped hits, classified: `recovery.go:86  handle(c, rec)` is a call of a *parameter* named `handle` (type `RecoveryFunc`,
declared at `recovery.go:53`), not of the method; the other skipped hits are the declaration, the parameter's declarations and pass-through (`recovery.go:40`, `:41`, `:53`) and
comments that use the word "handle" (`tree.go`, `ginS/gins.go`). The exported `Handle` (line 129) is a different identifier and is itself a caller (line 133).

### gin-04, callers: `Context.Get`
Key: `context.go::Context.MustGet`, `context.go::Context.ShouldBindBodyWith`, `context.go::Context.Value`,
`context.go::getTyped` (a generic function; its name carries no type parameter).

| Method | Result | Agree |
|---|---|---|
| 1 | rule `\bc\.Get\(`: 4 callers (lines 306, 313, 952, 1535) | yes |
| 2 | 4 `call` records at the same lines | yes |
| 3 | `gopls references context.go:297:19`: the same 4 outside tests | yes |

Skipped hits, each read for its receiver: `engine.pool.Get()` (`sync.Pool`, `gin.go:696`); `c.Request.Header.Get(...)`
(`http.Header`, `gin.go:813`, `context.go:1100`); `client.Get(url)` (`http.Client`, `test_helpers.go:45`); nine
`field.Tag.Get(...)` and `structField.Tag.Get(...)` (`reflect.StructTag`, `binding/form_mapping.go`); `header.Get(k)`
(`http.Header`, `render/reader.go:44`); `ps.Get(name)` (`Params.Get`, a different method, `tree.go:41`, in `Params.ByName`).

### gin-05, definition: `Engine.Handler`
| Method | Result | Agree |
|---|---|---|
| 1 | `rg '^func \(\w+ \*?Engine\) Handler\('`: one hit, `gin.go:257` (the same search without the type also finds `context.go:176`, the method of `Context`) | yes |
| 2 | `go/ast`: `gin.go` line 257, closes at 264, no doc comment; the `Context` one is `context.go:176` | yes |
| 3 | `gopls definition gin.go:578:29` (`engine.Handler()` in a struct literal) answers `gin.go:257` | yes |

### gin-06, callers: `setWithProperType` in `binding/form_mapping.go`
Key: `binding/form_mapping.go::setArray`, `binding/form_mapping.go::setByForm`, `binding/form_mapping.go::setWithProperType`
(the function calls itself at line 383). No call from any other file exists.

| Method | Result | Agree |
|---|---|---|
| 1 | rule `\bsetWithProperType\(` minus the `func` line: 3 callers (lines 319, 383, 492) | yes |
| 2 | 3 `call` records at the same lines | yes |
| 3 | `gopls references binding/form_mapping.go:323:6`: the same 3 outside tests | yes |

Disagreement on the first run (a fault in my harness, not in the code): Method 1 returned 0 callers because the rule had been
edited with a stray backspace character where `\b` was meant. A result of zero for a function with a visible caller was the
signal; I fixed the rule and re-ran everything, and all three then agreed.

### gin-07, callers: `responseWriter.WriteHeaderNow`, concrete receiver only
Key: `gin.go::Engine.handleHTTPRequest`, `gin.go::redirectRequest`, `gin.go::serveError`,
`response_writer.go::responseWriter.Flush`, `response_writer.go::responseWriter.Write`,
`response_writer.go::responseWriter.WriteString`.

| Method | Result | Agree |
|---|---|---|
| 1 | rule `\bc\.writermem\.WriteHeaderNow\(` or `\bw\.WriteHeaderNow\(`: 6 callers (`gin.go` 752, 807, 860; `response_writer.go` 85, 92, 137) | yes |
| 2 | 6 `call` records on `responseWriter.WriteHeaderNow`, plus 2 `iface-call` records on the interface method `ResponseWriter.WriteHeaderNow` (`context.go:224`, `context.go:1206`) | yes (the 2 are excluded by the question) |
| 3 | `gopls references response_writer.go:77:26`: **8** callers, the 6 above plus `context.go::Context.AbortWithStatus` and `context.go::Context.Render` | **no, by exactly those 2** |

Resolution by reading: `Context` declares `writermem responseWriter` (`context.go:62`, a concrete value) and
`Writer ResponseWriter` (`context.go:64`, an interface), and `reset` sets `c.Writer = &c.writermem` (`context.go:104`). The
calls at `context.go:224` and `:1206` are `c.Writer.WriteHeaderNow()`: they go through the interface, so at run time they
reach the concrete method, but statically their receiver is the interface. `gopls` reports references to a concrete method
together with calls through an interface it satisfies. The question states the rule (static type `responseWriter` or
`*responseWriter`; interface calls excluded), so the key is the 6. If interface dispatch were counted the key would be 8
(arithmetic: 6 + 2). A tool that follows interface dispatch will list the 2 extra names; whether to treat that as an error is
a scoring question settled here in advance: it is not credited as correct, and it lowers the Jaccard score.

### gin-08, definition: `node.getValue`
| Method | Result | Agree |
|---|---|---|
| 1 | `rg '^func \(\w+ \*?node\) getValue\('`: one hit, `tree.go:418` | yes |
| 2 | `go/ast`: `tree.go` line 418; doc comment starts at line 413; closes at 672 | yes |
| 3 | `gopls definition gin.go:744:17` (`root.getValue(...)` in `Engine.handleHTTPRequest`) answers `tree.go:418` | yes |

Partial credit window fixed in advance: lines 413 to 417 (the doc comment) earn 0.5; only 418 earns 1.0.

### gin-09, callers: `RouterGroup.GET`
Key: `ginS/gins.go::GET`, `routergroup.go::RouterGroup.StaticFS`, `routergroup.go::RouterGroup.staticFileHandler`.

| Method | Result | Agree |
|---|---|---|
| 1 | rule `\bgroup\.GET\(` or `\bengine\(\)\.GET\(`: 3 callers (`routergroup.go` 220, 247; `ginS/gins.go` 67) | yes |
| 2 | 3 `call` records at the same lines, no `iface-call` on `IRoutes.GET` | yes |
| 3 | `gopls references routergroup.go:142:27`: the same 3 outside tests | yes |

Resolution by reading, the reason this is not a plain grep question: `ginS/gins.go:67` is `engine().GET(...)`; in
`ginS/gins.go:14` `engine` is a package-level *variable* holding a function (`sync.OnceValue(func() *gin.Engine {...})`),
and `GET` on a `*gin.Engine` is the method promoted from the embedded `RouterGroup` (`gin.go:99-100`). The caller lives in a
different package from the target.

### gin-10, callers: `Context.Error` in `context.go`
Key: `context.go::Context.AbortWithError`, `context.go::Context.Render`.

| Method | Result | Agree |
|---|---|---|
| 1 | rule `\bc\.Error\(` restricted to `context.go`: 2 callers (lines 249, 1212) | yes |
| 2 | 2 `call` records in `context.go`; the two further callers are in `recovery.go` (excluded by the question) | yes |
| 3 | `gopls references context.go:261:19`, kept to `context.go`: the same 2 | yes |

Skipped hits, classified: `err.Error()` and `msg.Err.Error()` (method of the `error` interface), `msg.Error()` (method of
the `Error` struct, `errors.go:82`), `SliceValidationError.Error`, the type name `Error` and its uses, and the comment examples in
`errors.go`. `recovery.go:83` (inside a function literal) and `recovery.go:114` call `Context.Error` but are not in `context.go`.

## The pilot's third check

The three pilot questions were re-derived from scratch on a second shallow copy, fetched at 20261102 10:37 UTC into a new
directory, with `git rev-parse HEAD` again equal to the pin. The whole harness (all three methods, all ten questions) ran
there and its `m1.json`, `m2.json` and `m3.json` are byte-for-byte equal (`cmp`, exit 0 for each) to the first run's, so the pilot three
agree and so do all ten. The pilot bare-name hits (`handleHTTPRequest`, `hasRequestContext`, `handle`) were printed and read again on
the second copy, 20261102 10:42, with the same classification as above. The third check is on the same toolchain; it guards against a stale
or edited working tree and against an unrepeatable result, not against a flaw shared by the methods.

## Build tags, and candidates that were dropped

The module has files behind build tags (`nomsgpack`, `appengine`, `jsoniter`, `go_json`, `sonic`). Method 2 was run for the
default build and for `nomsgpack`, `appengine`, `jsoniter`, `go_json`, `sonic` and `nomsgpack,sonic`
(20261102 10:30 for the first two, 10:35 for the rest). For the seven callers targets the caller sets are identical in all of them; the declaration list is
identical for `nomsgpack` for the three definition targets. The questions assume the default build, and the question text says so.

Candidates considered and not used, all before any answer was written down in `questions.yaml`:

| Candidate | Why dropped |
|---|---|
| `binding.Default` (definition) | Two definitions, `binding/binding.go:95` (tag `!nomsgpack`) and `binding/binding_nomsgpack.go:91` (tag `nomsgpack`): the answer depends on a build tag |
| `Context.Set` (callers) | Three of its four callers (`BasicAuthForRealm`, `BasicAuthForProxy`, `Bind`) call it inside a returned function literal, which a tool may attribute differently |
| `Context.Abort` (callers) | One of five callers is inside a function literal (`CustomRecoveryWithWriter`) |
| `Context.reset`, `Engine.allocateContext` (callers) | Callers include `test_helpers.go`, a file made for testing that is not named `*_test.go`, so the exclusion rule would be ambiguous |
| `binding.validate` (callers) | Its caller set depends on the `nomsgpack` tag (11 callers by default, 10 with it) |

## Limits

- **Dynamic dispatch.** Calls through an interface value are not credited to a concrete method (gin-07 states this). A tool that
  resolves interface calls will list more names for gin-07 than the key. No other key is affected: of the 29 `iface-call` records, none is on an
  interface method that shares its name with another target (the interface methods called are `ResponseWriter.Size`, `.Status` and
  `.WriteHeaderNow`, and methods of the `binding`, `render` and `codec/json` interfaces).
- **Function values and callbacks.** A function stored in a variable and called later is not a direct call of the stored
  function. Only gin-09 passes through such a variable (`engine`), and there the callee is fixed by the variable's type.
  Handlers registered with `Use`, `GET` and the like are invoked by the router at run time; those edges are not in any key.
- **Reflection and generated code.** `binding/form_mapping.go` works through `reflect`; calls made by reflection do not
  appear. The only generated file, `testdata/protoexample/test.pb.go`, is outside the analysed packages and outside every key.
- **Function literals.** The question text says a call inside a function literal counts for the enclosing named function. No
  key depends on that rule (Method 2 records none of the 33 caller entries across the seven callers keys as being inside a
  literal; arithmetic: 4+11+4+3+6+3+2), so it is a stated convention, not a tested one.
- **Platform and build.** Analysed on darwin/arm64 with the default tags and the tag sets listed above. The only build
  constraints in the non-test source are the tags listed below (read with `rg '^//go:build'`) and one operating-system condition
  inside the `sonic` tag; there are no `_windows.go`-style file names. I did not run the analysis for another operating system.
- **Scope of "non-test source".** Files named `*_test.go`, and anything under `docs/`, `examples/`, `testdata/`, are excluded.
  `test_helpers.go` is included (it is not a `_test.go` file); no key involves it.
- **Callers versus call sites.** The key is a set of callers, not of call sites. In every key here each caller has exactly one
  call site (Method 2's records: 4, 11, 4, 3, 6, 3 and 2 sites for 4, 11, 4, 3, 6, 3 and 2 callers), so the distinction does not arise.
- **Not verified.** I did not run gin's own tests, did not read the whole repository, and did not compare against any tool the
  later step will test. The "random answerer scores near chance" and "perfect answerer scores 100%" checks of the scoring belong
  to the scoring step, not to this derivation. The type checker shared by Methods 2 and 3 was not tested for faults.
  `gopls` and `go/types` read the code as it compiles on this machine; a different Go version could in principle resolve
  something differently, though nothing here depends on a feature newer than `go 1.26.0`.

## Repeating three answers with stock tools

Install Go go1.27.3 and `gopls` v0.24.0 as above, fetch the pinned commit, then, inside the checkout (the language server
needs the module downloaded once, so allow it the module proxy):

| Question | Command | Expect |
|---|---|---|
| gin-02 | `gopls references context.go:1494:19` | four lines in `context.go` (1502, 1510, 1518, 1539) before the `_test.go` ones |
| gin-07 | `gopls references response_writer.go:77:26` | 8 non-test locations: 3 in `gin.go`, 3 in `response_writer.go`, 2 in `context.go` (the last two are the interface calls the key excludes) |
| gin-09 | `gopls references routergroup.go:142:27` | `routergroup.go:220`, `routergroup.go:247`, `ginS/gins.go:67` before the `_test.go` ones |
| gin-01 | `gopls definition gin.go:701:9` | `gin.go:719` |
| gin-03 (Method 1) | `rg -n --glob '*.go' --glob '!*_test.go' '\bhandle\(' .` | the definition at `routergroup.go:110`, 11 calls on `group.` in `routergroup.go`, and `recovery.go:86` which is the parameter, not the method |

Line and column are 1-based. The positions of every target: gin-02 `context.go:1494:19`, gin-03 `routergroup.go:110:27`,
gin-04 `context.go:297:19`, gin-06 `binding/form_mapping.go:323:6`, gin-07 `response_writer.go:77:26`, gin-09
`routergroup.go:142:27`, gin-10 `context.go:261:19` (declarations, for `gopls references`); gin-01 `gin.go:701:9`, gin-05
`gin.go:578:29`, gin-08 `gin.go:744:17` (call sites, for `gopls definition`).

Derived and written 20261102 10:41 UTC.
