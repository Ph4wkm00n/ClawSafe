# Branch Protection Setup

## Recommended `main` branch rules

Go to **Settings → Rules → Rulesets → New ruleset** (or **Settings → Branches → Add rule** for classic protection):

### Required settings:
- **Branch name pattern:** `main`
- **Require a pull request before merging:** Yes
  - Required approvals: 1
  - Dismiss stale reviews: Yes
- **Require status checks to pass:**
  - `backend` (CI workflow)
  - `frontend` (CI workflow)
  - `docker` (CI workflow)
- **Require branches to be up to date before merging:** Yes
- **Require conversation resolution before merging:** Yes
- **Do not allow bypassing the above settings:** Yes (or allow for admins only)

### Optional:
- **Require signed commits:** Recommended
- **Restrict who can push:** Limit to maintainers
- **Block force pushes:** Yes
- **Block branch deletion:** Yes

## Automated via GitHub CLI

```bash
gh api repos/Ph4wkm00n/ClawSafe/branches/main/protection \
  -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["backend","frontend","docker"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  -f restrictions=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```
