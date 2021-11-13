# md-sh

Minimalistic markdown placeholders filled by shell stdout

### Input Markdown file

<!--- #RUN OUTPUT echo -e "\`\`\`\n$(cat example.md)\n\`\`\`" -->

<!--- #ECHO OUTPUT { -->
```
# Files

<!--- #RUN OUTPUT ls | sed -e 's/^/\* /g' -->
<!--- #ECHO OUTPUT { -->
<!--- #ECHO } -->
```
<!--- #ECHO } -->

### Run generator

`python ./md-sh.py example.md`

### Generated Markdown file

<!--- #RUN OUTPUT echo -e "\`\`\`\n$(cat example_gen.md)\n\`\`\`" -->

<!--- #ECHO OUTPUT { -->
```
# Files

<!--- #RUN OUTPUT ls | sed -e 's/^/\- /g' -->
<!--- #ECHO OUTPUT { -->
- example_gen.md
- example.md
- Makefile
- md-sh.py
- README.md
<!--- #ECHO } -->
```
<!--- #ECHO } -->
