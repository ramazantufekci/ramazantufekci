from datetime import datetime

with open('README.template.md', 'r', encoding='utf-8') as f:
    template = f.read()

result = template.replace('{{formdate}}', datetime.now().strftime('%Y-%m-%d'))

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(result)