# X4, Flask: how the ten answers were derived

**Status: the answer key is frozen; nothing has been run against any agent or code-graph tool.** The questions and keys are in
[`questions.yaml`](questions.yaml). This page records where each answer came from, by two methods that do not share a
tool, and what the key does not cover. Written 20261102, UTC times below.

## The repository, as read

| Item | Value | Source and UTC read time |
|---|---|---|
| Repository | https://github.com/pallets/flask | task brief |
| Pinned commit | `49943b5a94413a530761350f04e896f76e8d620e` (default branch `main`) | `git rev-parse HEAD` after `git fetch --depth 1 origin <hash>` and checkout, 20261102 10:27 UTC; equals the pin in the brief; a second fresh clone at 10:37 UTC gave the same hash |
| Commit date | 2026-10-30 08:05:20 -07:00 = 2026-10-30 15:05:20 UTC (arithmetic) | `git log -1 --format=%cI`, 20261102 10:27 UTC; subject "add `versionchanged` for ctx signature change (#6176)" |
| Licence | BSD 3-Clause. `LICENSE.txt` at the commit is the three-condition BSD text headed "Copyright 2010 Pallets"; `pyproject.toml` at the commit also says `license = "BSD-3-Clause"` | both files read 20261102 10:27 UTC. The licence name comes from the text of the file (the three numbered conditions), the `pyproject.toml` line only agrees with it |
| Scope | `src/flask/`, 24 Python files, 9,566 lines | `find src -name '*.py'` and `wc -l`, 20261102 10:27 UTC. `find . -name '*.py' -not -path './src/*'` lists only files under `tests/`, `docs/` and `examples/`, which the questions exclude (run 20261102 between 10:30 and 10:40 UTC) |
| Tools | `python3` 3.15.2 (system), `ripgrep` 14.1.1, `git` 2.56.0 | version commands, 20261102 between 10:37 and 10:40 UTC |

Nothing from the repository was executed or imported: Flask was not installed. Everything below reads source text.

## Method 1: ripgrep and reading

For each question: search the whole repository for the name (`rg -n <name> .` or `rg -n -w <name> src`), read every hit, throw
away hits that are definitions, imports, docstrings, comments, keyword arguments or bare references, and find the
enclosing function of each remaining call with a text-only helper that walks up the indentation to the nearest `def` or
`class` line (no parser). The helper is a 20-line script kept in the scratch directory, `$SCRATCH/x4-flask/encl.py`. The
sets were saved in `$SCRATCH/x4-flask/m1/answers_m1.json` once the readings were done and before the comparison script was run.
The raw `rg` outputs are saved next to it (`$SCRATCH/x4-flask/m1/*.txt`).

## Method 2: the standard-library `ast` module

Three small programs, all kept in `$SCRATCH/x4-flask/`, none of them imports or runs Flask:

- `m2.py` parses every file under `src/` and, for each of the 1,223 call expressions, tries to resolve the callee to a
  definition in the repository. It follows `import` and `from ... import` (relative ones, and re-exports), `self` and `cls`
  with the inheritance chain (a left-to-right depth-first walk, not true C3 order), parameter and variable annotations,
  `x = SomeClass(...)`, return annotations, class attribute types (`self.a: T = ...`, `self.a = annotated_param`,
  `@property` returns) and annotated module globals such as `current_app: FlaskProxy`. It does **not** resolve `with ... as x`,
  `for x in ...`, values that come back from other packages, or anything dynamic.
  Outcome on the commit: 239 calls resolved to a repository function or method, 33 to a repository class (constructor),
  559 to something outside the repository (including builtins), 392 left unresolved (sum 1,223, arithmetic).
- `build_m2.py` takes, for each callers question, every call whose last name equals the asked name and accounts for each one:
  resolved to the target by the program, resolved to the target by a hand entry in `manual.json` (with the reason),
  resolved to something else, or left unresolved. It also lists every non-call mention of the same name found in the AST
  (values passed uncalled, parameters, attributes) so aliasing can be ruled out. It then maps each call to its outermost
  enclosing function or method.
- `m2_defs.py` answers the three definition questions from the same AST (every `def` and `class` of that name, the target of
  `flask.Blueprint` through the re-export, and the first class on `Flask`'s inheritance chain that defines `add_url_rule`).

A minimal version of the AST check, enough to reproduce most of the callers answers without the scratch directory (it
lists every call whose callee ends in NAME, with the enclosing `def` chain; it does not resolve shared names, so Q05, Q07
and Q09 still need the reading described below):

```python
# python3 -I callers.py REPO NAME
import ast, os, sys
repo, name = sys.argv[1:3]
def scan(tree, rel):
    def walk(node, chain):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                walk(ch, chain + [ch.name])
                continue
            if isinstance(ch, ast.Call):
                f = ch.func
                n = f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else None
                if n == name:
                    print(f"{rel}:{ch.lineno}  {'.'.join(chain) or '<module>'}  {ast.unparse(f)}")
            walk(ch, chain)
    walk(tree, [])
for dp, _, fs in os.walk(os.path.join(repo, "src")):
    for f in sorted(fs):
        if f.endswith(".py"):
            p = os.path.join(dp, f)
            scan(ast.parse(open(p, encoding="utf-8").read()), os.path.relpath(p, repo))
```

No code-graph tool and no knowledge-graph tool was used for any answer.

### What the two methods have in common (a limit on their independence)

The same person ran both in one session, so they are two methods, not two people. Order of work: an AST listing of all
call sites came first and was used to find candidate targets, so the targets were picked knowing roughly how many callers
they have (no agent result or tool result influenced the choice). The `rg` searches for q01 to q09 were run before
the resolver (`m2.py`) existed (the one for q10 was run after). Method 1 was finished before the program was run for q01, q02, q04 and q06; for q03 and
q05 to q10 the last step of Method 1 (finding the enclosing function of each call line) was done after the resolver's
per-name listing for the same name had been printed, so for those seven the readings are not blind to the program.
The two methods did not disagree anywhere (below), so the agreement shows that the reading and the program give the
same set, not that a third reader would. The three pilot questions got a separate third check on a fresh clone (below).

## Sites that Method 2 could not resolve and that were settled by reading

Five call sites were left unresolved by the program for a name that matched a target. Each was resolved by reading, and the
reason is in `manual.json`:

| Call site | Why the program could not resolve it | Reading |
|---|---|---|
| `src/flask/ctx.py:204`, `ctx.app.ensure_sync(f)` in `copy_current_request_context.wrapper` | `with original.copy() as ctx` | `AppContext.copy` and `AppContext.__enter__` both return `te.Self` (`ctx.py:355`, `ctx.py:506`), so `ctx` is an `AppContext`; `AppContext.__init__` stores `app: Flask` as `self.app` (`ctx.py:302`, `307`), so the callee is `Flask.ensure_sync` |
| `src/flask/sansio/blueprints.py:377`, `blueprint.register(app, bp_options)` | loop variable | `for blueprint, bp_options in self._blueprints`, with `self._blueprints: list[tuple[Blueprint, dict[str, t.Any]]]` (`sansio/blueprints.py:211`), and `Blueprint` there is the class in the same file, so it is `Blueprint.register` calling itself |
| `src/flask/cli.py:397`, `ctx.ensure_object(ScriptInfo).load_app()` | result of a call into click | click's `Context.ensure_object(self, object_type: type[V]) -> V` returns an instance of the class it is given. Source read: click 8.4.2 `src/click/core.py` line 748, fetched from the project's GitHub tag at 20261102 10:35 UTC. 8.4.2 is the click version in the repository's `uv.lock` at the pin. The file was read, not run |
| `src/flask/cli.py:623`, `info.load_app()` in `FlaskGroup.get_command` | `info = ctx.ensure_object(ScriptInfo)` (`cli.py:618`) | same signature as above |
| `src/flask/cli.py:645`, `info.load_app()` in `FlaskGroup.list_commands` | `info = ctx.ensure_object(ScriptInfo)` (`cli.py:640`) | same signature as above |

## Results, question by question

Names follow the key's format. "Agree" means the two sets are identical after mapping nested functions to the outermost
enclosing function or method. `compare.py` in the scratch directory performs that comparison; its last output line was
`ALL AGREE`.

### q01 (pilot, definition): `handle_url_build_error`

| | |
|---|---|
| Method 1 | `rg -n 'handle_url_build_error' .` gives 7 lines; the only `def` is `src/flask/sansio/app.py:982` (`rg -n '^\s*(async\s+)?def handle_url_build_error' src`); `src/flask/app.py:1259` is a call from `Flask.url_for`; the other hits are docstrings, a comment, `CHANGES.rst` and `tests/test_basic.py` |
| Method 2 | `m2_defs.py`: exactly one `def` of that name in the AST, `src/flask/sansio/app.py:982`, no decorator |
| Agree | yes |
| Third check (fresh clone) | `git grep` finds the same single definition, same line |
| Notes | the line is the `def` keyword's line (the signature continues on lines 983 and 984) |

### q02 (pilot, callers, 4): `get_debug_flag`

| | |
|---|---|
| Method 1 | `rg -n 'get_debug_flag' .` gives 11 lines (10 with `-w`): the definition (`helpers.py:28`), three imports, a test, and four call lines `app.py:723`, `cli.py:369`, `cli.py:972`, `sansio/app.py:493`. Enclosing functions: `Flask.run`, `ScriptInfo.load_app`, `run_command` (a top-level function under click decorators), `App.make_config` |
| Method 2 | 4 call sites resolved by the program through the imports `from .helpers import get_debug_flag` and `from ..helpers import get_debug_flag`; no other call with that last name; no non-call mention in `src/` |
| Agree | yes |
| Third check (fresh clone) | `git grep` call-expression pattern and the indentation walk give the same 4; `m2.py` rerun gives the same set |

### q03 (pilot, callers, 12): `Flask.ensure_sync`

| | |
|---|---|
| Method 1 | `rg -n 'ensure_sync' src` gives 27 lines: 1 definition (`app.py:1108`), 14 call lines and 12 lines that pass the method as a value (`_async_wrapper=self.ensure_sync`). The 14 calls sit in 12 outermost functions (listed in the key): ten call lines in nine `Flask` methods (`process_response` twice), `ctx.py:204` in the closure `copy_current_request_context.wrapper`, `views.py:110` and `116` in the closure `View.as_view.view`, `views.py:191` in `MethodView.dispatch_request` |
| Method 2 | 13 call sites resolved by the program (`self.ensure_sync` in `Flask`, `current_app.ensure_sync` through the annotated global `current_app: FlaskProxy`, whose class derives from `Flask`), 1 by hand (`ctx.py:204`, table above). The AST lists the same 12 non-call mentions |
| Agree | yes |
| Third check (fresh clone) | `git grep` call-expression pattern: 14 call lines, 12 outermost callers, identical; `rg` outputs for q01, q02, q03 are byte-identical between the two clones; `m2.py` and `build_m2.py` outputs identical |
| Notes | seven functions only pass the method as a value and are not callers: `Flask.full_dispatch_request`, `Flask.finalize_request`, `AppContext.push`, `AppContext.pop`, `flash`, `_render`, `_stream`. The question text says a reference is not a call; the `send(..., _async_wrapper=...)` calls hand it to the signal library (`blinker`, imported in `src/flask/signals.py`); whether and when that library calls it was not checked, and in any case it is not a direct call in `src/` |

### q04 (definition): the class behind `from flask import Blueprint`

| | |
|---|---|
| Method 1 | `rg -n '^\s*class Blueprint\b' .` finds two classes: `src/flask/blueprints.py:18` and `src/flask/sansio/blueprints.py:119`. `src/flask/__init__.py:3` is `from .blueprints import Blueprint as Blueprint`, and `src/flask/blueprints.py:18` is `class Blueprint(SansioBlueprint)` |
| Method 2 | `m2_defs.py` follows the re-export: `flask.Blueprint` resolves to `src/flask/blueprints.py:18` |
| Agree | yes |
| Notes | the answer needs the import line, a single search for `class Blueprint` returns two candidates |

### q05 (callers, 2): `send_from_directory` defined in `src/flask/helpers.py`

| | |
|---|---|
| Method 1 | `rg -n -w send_from_directory src` gives 9 lines. Excluded: the definition (`helpers.py:543`), a docstring mention (`helpers.py:437`), an example call inside that function's docstring (`helpers.py:554`, which the indentation walk reports as inside `send_from_directory`, read as docstring text), `helpers.py:582` (it calls `werkzeug.utils.send_from_directory`, another function), two imports and one re-export. Calls: `app.py:408` in `Flask.send_static_file`, `blueprints.py:100` in `Blueprint.send_static_file` |
| Method 2 | 2 call sites resolved to the target; the site at `helpers.py:582` resolves to the external `werkzeug.utils.send_from_directory` because the module does `import werkzeug.utils`; the AST ignores docstrings |
| Agree | yes |

### q06 (definition): `add_url_rule` found from a `Flask` instance

| | |
|---|---|
| Method 1 | `rg -n 'def add_url_rule' -B3 src` finds four definitions: `sansio/scaffold.py:376`, `sansio/app.py:606`, `sansio/blueprints.py:87` (`BlueprintSetupState`), `sansio/blueprints.py:413`. Classes: `Flask(App)` at `app.py:108` (defines no `add_url_rule`), `App(Scaffold)` at `sansio/app.py:60`. So `Flask`, then `App`: the method is `sansio/app.py:606`, decorated by `@setupmethod` on line 605 |
| Method 2 | `m2_defs.py` builds the chain `Flask`, `App`, `Scaffold` from the base-class expressions and takes the first class with the method: `src/flask/sansio/app.py:606`, decorator line 605 |
| Agree | yes |
| Notes | `rg -n 'add_url_rule\s*=|setattr' src` shows no assignment to `add_url_rule`; the only hits are a `__setattr__` definition (`ctx.py:59`) and two `setattr` calls (`app.py:305`, `306`), which act on the methods listed in `__init_subclass__` and only for user subclasses (limits below). The key accepts 605 and 606 because a definition can be reported at its decorator line or its `def` line |

### q07 (callers, 2): `Blueprint.register` of the sansio `Blueprint`

| | |
|---|---|
| Method 1 | `rg -n '\.register\(|\bregister\(' src` and reading: `tag.py:41` is in a module docstring; `tag.py:254` is `self.register(cls)` in `TaggedJSONSerializer.__init__`, a different method; `sansio/app.py:596` (`blueprint.register(self, options)` in `App.register_blueprint`) and `sansio/blueprints.py:377` (inside `Blueprint.register` itself, over `self._blueprints`) call the asked one |
| Method 2 | 1 site resolved by the program (`App.register_blueprint`, `blueprint` is annotated `Blueprint`), the `TaggedJSONSerializer.__init__` site resolved to the other class's method, 1 by hand (`sansio/blueprints.py:377`, table above) |
| Agree | yes |

### q08 (callers, 2): `load_dotenv` in `src/flask/cli.py`

| | |
|---|---|
| Method 1 | `rg -n load_dotenv src` gives 18 lines; whole-word matches are 11. Calls: `app.py:719` is `cli.load_dotenv()` in `Flask.run`, where `cli` is the module (`from . import cli`, `app.py:30`); `cli.py:510` is `load_dotenv(value, ...)` in `_env_file_callback`. The rest are the definition, `get_load_dotenv` (different name), the parameter `load_dotenv` of `Flask.run` and of `FlaskGroup.__init__`, the attribute `self.load_dotenv`, and docstrings |
| Method 2 | 2 call sites resolved by the program (one through the module alias `cli`); the non-call mentions found in the AST are the parameter and the attribute |
| Agree | yes |

### q09 (callers in `src/flask/cli.py`, 4): `ScriptInfo.load_app`

| | |
|---|---|
| Method 1 | `rg -n load_app src` gives 5 lines, all in `cli.py`: the definition (`:333`) and calls at `:397` (inside the closure `with_appcontext.decorator`, reported as `with_appcontext`), `:623` (`FlaskGroup.get_command`), `:645` (`FlaskGroup.list_commands`), `:954` (`run_command`). The receivers at 397, 623 and 645 come from `ctx.ensure_object(ScriptInfo)` |
| Method 2 | 1 site resolved by the program (`run_command`, whose `info` parameter is annotated `ScriptInfo`), 3 by hand (click's `ensure_object`, table above) |
| Agree | yes |
| Notes | all callers of this method are in `cli.py`, so the file scope removes nothing here |

### q10 (callers in `src/flask/app.py`, 2): `_CollectErrors.raise_any`

| | |
|---|---|
| Method 1 | `rg -n raise_any src` gives 4 lines: the definition (`helpers.py:676`) and calls at `app.py:1507` (`Flask.do_teardown_request`), `app.py:1540` (`Flask.do_teardown_appcontext`), `ctx.py:504` (`AppContext.pop`). In each of the three, the receiver is a local `collect_errors = _CollectErrors()` (`app.py:1496`, `app.py:1531`, `ctx.py:486`). The file scope keeps the two in `app.py` |
| Method 2 | 3 call sites resolved by the program through the local assignment; 2 of them are defined in `src/flask/app.py` |
| Agree | yes |
| Notes | the whole-repository answer is 3; the key is the 2 in `app.py` |

## A check that Method 2 can tell cases apart

Method 2's program was run on a throwaway copy of `src/` (in the scratch directory) with three functions appended: a new
caller of `get_debug_flag`, a function calling `register` on a new class that has its own `register` method, and a function
calling `register` on a `Blueprint`-typed parameter. The new caller of `get_debug_flag` and the `Blueprint`-typed call
appeared in the answers (5 and 3 callers instead of 4 and 2) and the call on the other class did not. The repository
itself was not changed. This shows the resolver separates same-named methods when the receiver is typed; it does not show
that it finds every caller in untyped code, which is why unresolved sites are listed and read.

## Candidates that were dropped, and why

| Candidate | Reason |
|---|---|
| `ProxyMixin._get_current_object` (10 call sites) | its only definition is a type-checking-only protocol stub in `globals.py`; the real method belongs to werkzeug's `LocalProxy` |
| `locate_app`, `stream_with_context` | `@overload` stubs give three `def` lines for one function, so a definition question has no single line |
| `JSONProvider.dumps` / `loads` and `add_url_rule` callers | calls go through `self` or `current_app.json` to an overridable method, so the static target is not one definition; the callers would depend on dynamic dispatch |
| `Scaffold._method_route` (6 callers) | clean, but all six callers are neighbouring methods in one class; kept in reserve as a callers question in the 6 to 15 range |
| `Blueprint.record_once` (10 callers) | clean, one caller is a nested closure; kept in reserve |

## What the key does not cover

- **Dynamic behaviour.** Static reading only. Calls through `getattr` (for example `MethodView.dispatch_request` picks
  `get`, `post` and so on by name), callbacks that other code may invoke later (`_async_wrapper=self.ensure_sync` is handed to the signal
  library; Jinja filters, click callbacks and view functions registered with `add_url_rule` are further examples), overridable methods called
  through `self` (virtual dispatch), and subclasses outside the repository are not in the key. A "caller" here is a call
  expression in `src/flask/` whose callee resolves to the asked definition.
- **Runtime rewriting.** `Flask.__init_subclass__` (`app.py:251` to `306`) wraps methods of user subclasses with
  `setattr` when they still use the signature from before the `ctx` parameter was added (its comment, and the
  `versionchanged:: 3.2` note on `do_teardown_request`). It does not change which function a call expression in `src/` names.
- **Decorators.** `@setupmethod`, click and similar decorators wrap functions; the key names the decorated `def`.
- **Convention.** A call inside a nested function is attributed to the outermost enclosing function or method. This is a
  rule of this question set, written into every callers question, not a fact about Python.
- **Generated and dynamically loaded code.** No generated source file found (`rg -n -i 'auto-?generated|do not edit|generated by|@generated' src`
  returns nothing). Dynamic loading exists and is outside the key: `exec(compile(...))` of user files (`config.py:209`,
  `cli.py:1022`), plugin commands from entry points (`cli.py:604`), and module-level `__getattr__` for deprecated names
  (`ctx.py:528`, `globals.py:65`). It runs user code; none of those lines names a function the questions ask about.
- **Not verified.** Nothing was executed, so no runtime check confirms any answer (no test run, no tracing). Click's
  `ensure_object` was read in version 8.4.2 (the lock file's version), not in whatever version a later run installs. The
  documentation under `docs/` was not read for conflicting statements. The scoring rules in `questions.yaml` were written and
  parsed (the file loads as YAML and its answers equal the Method 1 sets) but no scoring program was written or tested. The
  question wording was not tested on any agent, so it may still be misread; the `why_not_trivial` lines are descriptions of
  what makes a plain search ambiguous, measured by `rg` counts, not predictions about any agent or tool.

## Reproducing three answers

`$REPO` is a fresh checkout at the pinned commit:

```
git init -q repo && cd repo && git remote add origin https://github.com/pallets/flask.git
git fetch -q --depth 1 origin 49943b5a94413a530761350f04e896f76e8d620e && git checkout -q FETCH_HEAD
git rev-parse HEAD        # must print 49943b5a94413a530761350f04e896f76e8d620e
rg -n 'handle_url_build_error' . ; sed -n 982p src/flask/sansio/app.py                       # q01
python3 -I callers.py . get_debug_flag                                                       # q02: 4 lines
python3 -I callers.py . ensure_sync | wc -l                                                  # q03: 14 call lines, 12 outermost callers
python3 -I callers.py . raise_any                                                            # q10: 3 lines, 2 in src/flask/app.py
```
