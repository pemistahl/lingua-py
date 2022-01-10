poetry run pdoc --html --force --config show_source_code=False --template-dir=pdoc-templates --output-dir=docs lingua
mv docs/lingua/* docs
rmdir docs/lingua
