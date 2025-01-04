# Upgrade

::: info INFO
Every time you run gcop command, it will check if there is a new version of GCOP. If there is a new version, it will ask you if you want to update.
:::

This section will guide you through the process of upgrading GCOP to the latest version.

Install the latest version of GCOP:

```bash
pip install gcop -U
```

Then, run the following command to initialize GCOP and migrate your config file if exists:

```bash
gcop init
```

Then, you can use GCOP as usual.

::: info INFO
After `v1.6.0`, the config file location has been changed to `~/.zeeland/gcop/config.yaml`. Run `gcop init` to migrate your config automatically if exists.
:::
