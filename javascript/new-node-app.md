# New Node App

## Configuration

```shell
npm config list | grep init
```

Add this function to your shell profile (.profile, .bashrc, .zshrc etc.)

```bash
function npm-init-config {
  npm config set \
    init-author-name="Your Name" \
    init-author-email="you-email@mailprovider.tld" \
    init-author-url="https://your-website.tld" \
    init-license="MIT" \
    init-version="0.0.1"
}
```

## CLIs

1. React
2. Angular
3. Plain

## React

https://create-react-app.dev

```shell
npx create-react-app my-app
```

## Angular

https://angular.dev/tools/cli

```shell
npm install -g @angular/cli
```

```shell
ng new my-app
```

## Plain

Add this function to your shell profile (.profile, .bashrc, .zshrc etc.)

```shell
function node-project {
  if [ $# -ne 1 ] && echo "No project specified" && return 1
  [ -d ${1} ] && echo "Project already exists" && return 1
  mkdir -p ${1}
  cd ${1}
  git init
  npx --yes license $(npm config get init-license) -o "$(npm config get init-author-name)"
  npx --yes gitignore node
  npx --yes covgen "$(npm config get init-author-email)"
  npm --yes init
  git add -A
  git commit -m "Initial commit"
}
```