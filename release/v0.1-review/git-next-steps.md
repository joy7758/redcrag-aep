# Git Next Steps

## Current Git State

At Phase 16, `git status --short` reported that the directory is not a git repository.

## Do Not Do Automatically

- do not run `git init` automatically
- do not create commits automatically
- do not create tags automatically
- do not push to any remote automatically

## Recommended Manual Path

1. Decide whether this directory should become a git repository.
2. If yes, run `git init` manually.
3. Review `.gitignore`.
4. Run `python3 demo/run_all.py`.
5. Run `python3 scripts/acceptance_check.py`.
6. Add files intentionally.
7. Create an initial commit manually.
8. Optionally tag `v0.1-review` manually.
9. Optionally connect to a remote repository manually.

## Suggested Commit Message

```text
Initialize risk-linked AEP v0.1 review release
```

## Suggested Tag Name

```text
v0.1-review
```

## Git Boundary

Git operations are intentionally left as manual decisions because they affect repository history and external sharing.
