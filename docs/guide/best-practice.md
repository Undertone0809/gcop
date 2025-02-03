# Best Practice

There are some best practices for using GCOP.

## Commit All Changes

If you want to commit all changes, you can use the following command:

```bash
git ac
```

The command is the same as `git add . && git commit`.


If you want to commit all changes and push to the remote repository, you can use the following command:

```bash
git acp
```

The command is the same as `git add . && git commit && git push`.

## Revert a Regretful Commit Pushed to the Remote Repository

If you have just committed incorrect commit information and have already pushed it to the remote repository, you can use the following commands to revert the regretful commit:

```bash
git undo
git pf
```

The command is the same as `git reset HEAD~ && git push --force`.

This means that you are reverting the regretful commit, which will result in one less commit locally. Then, through `pf`, you push force to the remote repository, equivalent to your previous commit never happening.

## Amend a Commit

If you have already committed, but forgot to add some files, you can use the following command to add the files:

```bash
git add <file>
git amend
```

The command is the same as `git commit --amend`.
