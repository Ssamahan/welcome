# Apply the review fixes

Three patches, one per repository. Everything was built and verified locally, but the
GitHub token in this session is **read-only**, so nothing has been pushed. Apply these
wherever you have push access.

| Patch | Repository | Commit message already written |
| --- | --- | --- |
| `lab-fixes.patch` | `Ssamahan/lab` | schema, deletion, visitor, CI, Android, CSP |
| `lab-server-fixes.patch` | `Ssamahan/lab-server` | published credentials, auth, CORS, TLS |
| `welcome-fixes.patch` | `Ssamahan/welcome` | HTML site instead of Markdown |
| `lab-tests-followup.patch` | `Ssamahan/lab` | **apply 2nd** — two assertions that failed for the wrong reason |
| `lab-perf-budget.patch` | `Ssamahan/lab` | **apply 3rd** — bundle budget measured as bytes shipped + time |

---

## Option A — apply to a fresh clone

```bash
git clone git@github.com:Ssamahan/lab.git ~/fix-lab
cd ~/fix-lab && git checkout -b fix/review
git am ~/patches/lab-fixes.patch \
       ~/patches/lab-tests-followup.patch \
       ~/patches/lab-perf-budget.patch      # order matters
git push -u origin fix/review
cd ~

for repo in lab-server welcome; do
  git clone git@github.com:Ssamahan/$repo.git ~/fix-$repo
  cd ~/fix-$repo && git checkout -b fix/review
  git am ~/patches/$repo-fixes.patch
  git push -u origin fix/review
  cd ~
done
```

Then open a pull request from `fix/review` in each repository. The `welcome` patch is
only `index.html` + `README.md`; the other two are larger.

## Option B — patch the existing checkout

```bash
cd /path/to/lab && git checkout -b fix/review && git am /path/to/lab-fixes.patch
```

`git am` keeps the author and the commit message. If a patch does not apply because
`main` has moved, `git am -3` will try a three-way merge.

---

## Order of operations, and why

**1. Rotate the `lab-server` credentials first — before deploying the code.**

The published `JWT_SECRET` and `ADMIN_PASSWORD` are live seams *right now*. The new
server refuses to start with either of them, so this is also the step that cannot be
skipped:

```bash
cd lab-server
npm install
npm run secret                     # JWT_SECRET
npm run hash -- "a long password"  # ADMIN_PASSWORD_HASH
```

Put both into Render → Environment, plus `DATABASE_URL` and `ALLOWED_ORIGIN`.
**Remove `DB_PATH` and `ADMIN_PASSWORD`; they are no longer read.**

> Rotating `JWT_SECRET` invalidates every token, so any client holding one must sign in
> again. That is the point — assume the old ones are public.

**2. Run `supabase/schema.sql` in the Supabase SQL editor.**

It is idempotent (`if not exists`, `drop policy if exists`), so re-running is safe. It
removes the `anon` DELETE grant.

> **Nobody can delete a month online until you populate the allowlist.** That is
> deliberate — an empty list is the safe default. When you want it back:
> ```sql
> insert into private.lab_writers (writer, note)
> values ('your-supabase-user@email', 'Laboratory manager');
> ```
> `writer` is the `email` claim of the signed-in Supabase user. The console tells the
> operator this in plain words if it is refused.

**3. Deploy `lab`.**

Pages republishes on push. The CSP goes live with `index.html`. If a screen goes blank,
the CSP is the first suspect — check the browser console for a `Refused to…` line and
tell me exactly which directive fired; it is a one-line addition.

**4. Check the Android build.**

`npm run build` now produces `www/`. `npx cap add android` runs on the first CI build.

---

## What to verify afterwards

```bash
# lab-server: the gate
cd lab-server && npm test            # 21 tests, no database needed

# lab: everything
cd lab && node harness/run-all.js    # 91 pass locally; CI also runs the 3 browser suites

# lab: the schema, against the real PostgreSQL grammar
pip install pglast && python -c "
from pglast import parse_sql; import glob
[parse_sql(open(f).read()) for f in glob.glob('supabase/*.sql')]; print('all parse')"
```

Locally the harness reports **91 passed / 13 failed / 3 skipped**. The 13 are real,
pre-existing product behaviours I did **not** change because each one alters what the
laboratory sees — they need your decision, not a quiet fix:

| Suite | What it wants |
| --- | --- |
| `fifo82` | the training queue ordering and the days-waited figures |
| `training_warning149` | no conflict warning once coverage is resolved |
| `history85` | the two readings of Monthly Reports |
| `round49` | ISO readiness rows |
| `reach91`, `report83`, `sync122`, `navigation126`, `startup127`, `equipment123` | offline reach, copy wording, navigation |

The 3 skipped (`browser-*`) need `libnss3` and friends; CI installs them.

`perf109` and `zeros93` are **fixed** in the follow-up patches. The FBC failure was
never a product bug — the suite hand-edited a figure, then silently failed to restore
it and checked the page anyway. The size budget now measures compressed bytes and
states the cost as seconds on 3G: *first screen 269 KB → 1.7 s*, against a 300 KB /
6 s limit that still fails when the bundle grows.

---

## Nothing here can lock you out

- **Your login is untouched.** No password, role or permission for `u1` was changed.
- **`u1` keeps the names open**, as you asked: `A.namesOpen()` returns true for the
  owner account for the whole session. Staff on other accounts still mask until they
  open names.
- **Offline devices keep syncing.** `anon` still holds SELECT/INSERT/UPDATE on the
  register; only DELETE moved behind the allowlist.
- **No data is deleted.** The staff roster dumps and the `.b64.txt` files are untracked,
  not removed from disk, and the Supabase tables are untouched.
- **The visitor view loses nothing it legitimately had** — it reads the register and
  exports what it read. It simply can no longer open Staff & Settings.
