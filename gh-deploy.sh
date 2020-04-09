cd mohsinmdl.github.io/
# cp -r ../simpledoc/docs/ docs/
cp -Rv ../simpledoc/docs/ ./
sleep 2
mkdocs gh-deploy --config-file ../simpledoc/mkdocs.yml --remote-branch master
