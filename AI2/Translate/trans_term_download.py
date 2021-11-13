import boto3
import urllib
translate = boto3.client('translate')
result = translate.get_terminology(
    Name='term_ja', TerminologyDataFormat='CSV')
url = result['TerminologyDataLocation']['Location']
print(url)
with open('term_ja_download.csv', 'wb') as file_out:
    with urllib.request.urlopen(url) as file_in:
        file_out.write(file_in.read())
