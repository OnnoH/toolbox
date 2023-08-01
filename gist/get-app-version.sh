# Instead of awking, jqing, seding etc. This looks like the most efficient and portable

node -pe "require('./package.json').version"

# This works too, but may take longer to start

npx -c 'echo "$npm_package_version"'