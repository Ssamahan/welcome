# Pushing the fixes — terminal guide

Everything below was run in a Linux sandbox before it was written down, including the
`git am` of all three patch sets onto a fresh clone. Your name and email are already
filled in: **Kelvin SAMAHANI · smhnklvn@gmail.com**.

Total time: about 20 minutes, most of it waiting for Render and Pages to redeploy.

---

## 0. What you are pushing

| Repository | Patches (in this order) |
| --- | --- |
| `lab` | `lab-fixes.patch` → `lab-tests-followup.patch` → `lab-perf-budget.patch` |
| `lab-server` | `lab-server-fixes.patch` |
| `welcome` | `welcome-fixes.patch` |

You need the files from the `patches/` folder next to this document. Put them in
`~/patches`:

```bash
mkdir -p ~/patches
# copy the six files from patches/ into ~/patches (file manager, or scp from wherever
# you downloaded them), then:
ls -lh ~/patches
```

You should see all six `.patch` files. If two are missing, stop — the guide assumes all
five patches are present (three for lab, one for lab-server, one for welcome, plus the
tests follow-up).

---

## 1. Set up git once (5 minutes, never again)

### 1.1 Tell git who you are

```bash
git config --global user.name  "Kelvin SAMAHANI"
git config --global user.email "smhnklvn@gmail.com"
git config --global init.defaultBranch main
```

Verify:

```bash
git config --global --get user.email      # smhnklvn@gmail.com
```

> **Why this matters:** `git am` reads the author from your config. Without it, every
> patch stops with `fatal: empty ident name` — I hit exactly that while testing.

### 1.2 Authenticate to GitHub without ever typing a password

GitHub no longer accepts account passwords over git. Use a **personal access token**
(PAT) — it is a long string you paste once and the credential helper remembers.

**Create the token:** <https://github.com/settings/tokens> → *Generate new token
(classic)* → expiry 90 days → tick **`repo`** (and `workflow`, because the patches add
GitHub Actions files) → *Generate* → **copy it now**, it is shown once.

**Store it once:**

```bash
git config --global credential.helper store
```

The first `git push` will ask:

```
Username for 'https://github.com': smhnklvn
Password for 'https://smhnklvn@github.com': <paste the token, not your password>
```

After that it is remembered in `~/.git-credentials` (mode 600). To use a built-in
keyring instead of a plain file (GNOME, KDE):

```bash
sudo apt install libsecret-1-0 libsecret-1-dev
git config --global credential.helper libsecret
```

**Alternative — SSH keys** (better long-term, no token to expire):

```bash
ssh-keygen -t ed25519 -C "smhnklvn@gmail.com" -f ~/.ssh/id_ed25519 -N ""
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub      # paste into https://github.com/settings/keys → New SSH key
```

Then use `git@github.com:Ssamahan/lab.git` instead of `https://github.com/...` in every
clone below, and skip 1.2's token.

### 1.3 Sanity check

```bash
git ls-remote https://github.com/Ssamahan/lab.git HEAD
```

If it prints a commit hash, you are authenticated for reading. Writing is tested by the
first `git push`.

---

## 2. `lab-server` — do this one FIRST

The published `JWT_SECRET` and admin password are live right now. Rotate them before
anything else touches that repo.

### 2.1 Clone and apply

```bash
cd ~
git clone https://github.com/Ssamahan/lab-server.git
cd lab-server
git checkout -b fix/security
git am ~/patches/lab-server-fixes.patch
```

You should see:

```
Applying: fix(security): remove published credentials, require auth, verify TLS, Postgres-only
```

### 2.2 Prove it works before pushing

```bash
npm install
npm test
```

Expect **`# pass 21` / `# fail 0`**. Then check the guard that blocks the leaked secret:

```bash
node server.js
```

Expect it to refuse and exit:

```
FATAL: refusing to start. Missing required environment variable(s): JWT_SECRET, ADMIN_PASSWORD_HASH, DATABASE_URL, ALLOWED_ORIGIN
```

That is the fix working. It will not run on a default any more.

### 2.3 Generate your real credentials (keep these private)

```bash
npm run secret
# → JWT_SECRET=mbfY56/....

npm run hash -- "PUT-A-LONG-PASSWORD-HERE"
# → ADMIN_PASSWORD_HASH=$2a$12$....
```

Use your own long password — 12+ characters, stored in a password manager. The hash is
what goes to Render; the password itself never leaves your machine.

### 2.4 Push

```bash
git push -u origin fix/security
```

Then open a pull request:

```bash
# if you have the GitHub CLI:
gh pr create --fill --base main --head fix/security

# otherwise open the link git printed and press "Create pull request"
```

Merge it (on GitHub: *Merge pull request*). Or, if you would rather go straight to main:

```bash
git checkout main && git merge fix/security && git push origin main
```

> **Merge first, deploy second.** The new server refuses to start until the four
> environment variables exist, so if you deploy before configuring Render, the service
> goes down. Next step prevents that.

### 2.5 Configure Render (before or immediately after merging)

Render dashboard → your service → **Environment**:

| Key | Value |
| --- | --- |
| `JWT_SECRET` | the `npm run secret` output |
| `ADMIN_PASSWORD_HASH` | the `npm run hash` output — **the whole `$2a$12$…` string** |
| `DATABASE_URL` | your Neon URL, keep `?sslmode=require` |
| `ALLOWED_ORIGIN` | `https://ssamahan.github.io` |
| `EMAIL_USER` | `rulidhlab@gmail.com` (optional) |
| `EMAIL_PASS` | Gmail app password, 16 chars (optional) |
| `EMAIL_FROM` | `Ruli Lab Systems <rulidhlab@gmail.com>` (optional) |

**Delete these two** — they are no longer read, and leaving `ADMIN_PASSWORD` there is a
liability:

- `ADMIN_PASSWORD`
- `DB_PATH`

Save → Render redeploys. The log should show:

```
✅ Ruli Lab Server v2.0.0 online port 10000 db=postgres email=true
```

If it exits instead, read the `FATAL:` line — it names the variable that is wrong. The
most common one: the bcrypt hash got mangled by shell quoting. It must start with `$2a$`
or `$2b$` and be pasted whole.

Health check: <https://lab-server-7hwd.onrender.com/api/health> should return
`{"ok":true,"ready":true,"dbType":"postgres","persistent":true}`.

---

## 3. Supabase — run the schema (5 minutes)

This is what stops anyone with the publishable key from deleting your monthly returns.

1. Open <https://supabase.com/dashboard> → project **`lkjwztvhmzhasclmlocx`**.
2. **SQL Editor → New query**.
3. Paste the **whole** of `supabase/schema.sql` from the `lab` repo (after you apply the
   patch in step 4, or from the patch itself).
4. **Run**.

It is safe to re-run — every statement is `if not exists` / `drop policy if exists`.

**What changes:**

- `anon` loses `DELETE` on `lab_report_months` (it could erase your returns before).
- Reads and writes stay exactly as they are, so every offline phone keeps syncing.
- Deletion now goes through `public.lab_month_delete()`, which checks a list.

**Re-enable deletion for yourself** — until you do this, nobody can delete a month
online. That is the safe default, not a bug. Run:

```sql
-- who is allowed to delete a monthly return
insert into private.lab_writers (writer, note)
values ('smhnklvn@gmail.com', 'Kelvin SAMAHANI — Laboratory Manager')
on conflict (writer) do nothing;

select * from private.lab_writers;
```

`writer` matches the signed-in Supabase user's `email` claim — so use the email of the
project account the console signs in with (Authentication → Users), not necessarily the
one above. If you sign in anonymously, add `auth.jwt() ->> 'sub'` style values instead,
or turn anonymous sign-ins off and use a real user.

Verify the ceiling works (optional, proves the guard):

```sql
-- as anon this would now fail with 42501
select public.lab_month_delete('1999-01');
```

---

## 4. `lab` — the console

### 4.1 Clone and apply all three, in order

```bash
cd ~
git clone https://github.com/Ssamahan/lab.git
cd lab
git checkout -b fix/review
git am ~/patches/lab-fixes.patch
git am ~/patches/lab-tests-followup.patch
git am ~/patches/lab-perf-budget.patch
```

Expect three `Applying:` lines. **Order matters** — the follow-ups edit files the first
patch creates.

If one fails with `Patch does not apply`, your `main` has moved. Try a three-way merge:

```bash
git am --abort
git am -3 ~/patches/lab-fixes.patch
```

### 4.2 Verify before pushing

```bash
cd harness && npm install && cd ..
node harness/run-all.js
```

Expect roughly **`91 passed · 13 failed · 3 skipped`**. The 13 are pre-existing product
behaviours listed in `patches/README.md` — they fail on `main` too, so they are not your
regression. The 3 skipped need Chromium libraries; that is an environment matter, not a
failure.

Quick targeted check of what the patches fixed:

```bash
node harness/run-all.js zeros93 perf109 csp164 visitor164 sync89
```

All five should pass.

Also check the SQL parses (optional but worthwhile):

```bash
python3 -m venv .venv && .venv/bin/pip install -q pglast
.venv/bin/python -c "
from pglast import parse_sql; import glob
[parse_sql(open(f).read()) for f in glob.glob('supabase/*.sql')]; print('all SQL parses')"
```

### 4.3 Push and merge

```bash
git push -u origin fix/review
gh pr create --fill --base main --head fix/review     # or use the web link
```

Merge. GitHub Pages redeploys in a minute or two: <https://ssamahan.github.io/lab/>

**What to check after it goes live:**

- The console opens (a Content-Security-Policy is now enforced). If a screen goes
  blank, press `F12` → Console and look for a line starting `Refused to`. Send me the
  directive name; it is a one-line addition to the `<meta http-equiv="Content-Security-Policy">`.
- **Sign in as yourself** — names should be visible without pressing "Show names"
  (your account `u1` has them open for the session).
- Open **Staff & Settings** in the visitor view in a private window: it should now say
  *"This area is not open to the visitor view."*

### 4.4 The Android build (optional)

The patches also fixed the APK pipeline. On the next push to `main`, **Actions → Build
APK** runs (`apk.yml`, which used to sit at the repo root where GitHub never read it).
Java 21, `npm run build` producing `www/`, then Gradle. Download the artifact from the
run summary.

---

## 5. `welcome` — the website

```bash
cd ~
git clone https://github.com/Ssamahan/welcome.git
cd welcome
git checkout -b fix/site
git am ~/patches/welcome-fixes.patch
git push -u origin fix/site
```

Merge, and within a minute <https://ssamahan.github.io/welcome/> is a real page:
responsive, a click-to-load video instead of an escaped `<iframe>`, no "p9 Copyright"
line, working Instagram and email links.

> **Note:** this repository's `main` now also contains a `patches/` folder with these
> same files, committed on the working branch `arena/40a43de5-welcome`. That is only so
> you can download them — delete it after you have them, it does not belong on the site:
> ```bash
> git rm -r patches && git commit -m "chore: remove temporary patch drop" && git push
> ```

---

## 6. Order summary

1. `lab-server` — push, merge, **configure Render**, confirm health.
2. **Supabase** — run `schema.sql`, then add yourself to `private.lab_writers`.
3. `lab` — push, merge, check Pages and sign in.
4. `welcome` — push, merge.

Doing 1 and 2 before 3 means no device is ever left unable to delete with no way back.

---

## 7. Troubleshooting

| Message | Cause | Fix |
| --- | --- | --- |
| `fatal: empty ident name` | git has no name/email | step 1.1 |
| `Authentication failed` on push | password used instead of token | step 1.2 |
| `Support for password authentication was removed` | same | step 1.2 |
| `Patch does not apply` | `main` moved | `git am -3`, or `git am --abort` then re-clone |
| `FATAL: JWT_SECRET must be at least 32 characters` | truncated paste | regenerate with `npm run secret` |
| `FATAL: ADMIN_PASSWORD_HASH must be a bcrypt hash` | shell ate the `$` | quote it: `'$2a$12$…'` |
| `FATAL: database unreachable` | Neon URL wrong or paused | copy it again from Neon; free projects pause when idle |
| Render service exits on deploy | env vars missing | step 2.5 — the log names the variable |
| Console blank after deploy | CSP blocked something | `F12` → Console → send me the `Refused to` line |
| `refused to delete` in the console | not on the allowlist | the SQL in step 3 |

---

## 8. Checking it worked

```bash
# lab-server: no secret in the repo, tests green
cd ~/lab-server && npm test | tail -3
grep -rn "nURevk1nqhtDsR39sYlS9tP16sdRafL35SzQhoiDQOI" . && echo "STILL PUBLISHED" || echo "secret gone"

# lab: the schema runs, the suites pass
cd ~/lab && node harness/run-all.js | tail -3

# welcome: the site is HTML, not Markdown
cd ~/welcome && test -f index.html && echo "index.html present"
```

Health of the live server:

```bash
curl -s https://lab-server-7hwd.onrender.com/api/health
```

---

## 9. If you would rather not use patches at all

The patches are ordinary commits. Once applied in a clone, you can also read them as
diffs before pushing:

```bash
git log --stat main..HEAD          # what changed
git show HEAD                      # the last one in full
```

And if anything looks wrong, you can throw the branch away without affecting `main`:

```bash
git checkout main && git branch -D fix/review
```

Nothing is forced, nothing rewrites history, and `main` is untouched until you merge.
