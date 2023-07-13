# GUIDE to install yarn, nvm (node) on macOS

> last update: Jul 2019

## Assumptions:

- macOS >= 10.14 (Mojave)
- [homebrew](https://brew.sh) properly installed

## Prepare before setup (cleanup)

```
brew uninstall --force yarn node npm  # remove previously installed node, npm, yarn
brew cleanup  # clean all broken symlinks and "waste" (not really required as of homebrew 2019)
brew update  # always good to have the latest
```

### Cleanup previously installed node/npm config

If you used the instructions [provided in this gist](https://gist.github.com/rcugut/c7abd2a425bb65da3c61d8341cd4b02d), then you need to do some more cleanup:

1. in `~/.bashrc`:

```
# remove all the lines below:
export NPM_PACKAGES....
export NODE_PATH....
# and remove all references to these variables later in the file
```

2. delete ".npmrc": `rm -f ~/.npmrc`

3. delete all existing installed global npm packages (! but make sure to write down if you're using any of them, to reinstall afterwards)

```
# !!! DESTRUCTIVE COMMAND, PAY ATTENTION !!!
sudo rm -rf /usr/local/npm_packages   #  !!! MAKE SURE YOU COPY THIS LINE WITH FULL ABSOLUTE PATH COMPLETELY !!!
```

## Install yarn via homebrew

```
# install Yarn w/o the node dependency
# https://github.com/yarnpkg/website/blob/13e95d80282f028ed7b28a822818ce128ea70b7e/lang/en/docs/_installations/mac.md
brew install yarn --ignore-dependencies  # the option --without-node doesn't seem to work anymore >= Feb 2019
```

## Install [`nvm`](https://github.com/creationix/nvm)

Always consult the latest [README (Install section)](https://github.com/nvm-sh/nvm#installation-and-update)

Install nvm version 0.34.0 (current on Jul 2019)

```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
```

Install node latest lts (`dubnium`, v10.x, current on Jul 2019)

```
nvm install lts/dubnium
```

Set nvm to use latest LTS as default for new bash sessions

```
echo "lts/dubnium" > .nvmrc #  default to the latest LTS version
nvm alias default lts/dubnium
```

### RESTART all terminals => you're done ;-)

## IMPORTANT NOTES

**NEVER use `sudo`** in any of the commands issued with `node`, `yarn`, or `npm`. If you need global packages installed, just follow nvm guidelines, and do `yarn global add <package>` or `npm install -g <package>`.

#### EXTRA: add fancy bash prompt to show ruby and node versions

...TODO...
see `.git-prompt-colors.sh`
