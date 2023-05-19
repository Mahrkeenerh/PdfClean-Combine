import os

import pypdf


files = os.listdir('.')
pdf_files = [f for f in files if f.endswith('.pdf') and f != 'combined.pdf']
if len(pdf_files) == 0:
    print('No pdf files found.')
    exit()
print(f'pdf_files: {pdf_files}')
if 'combined.pdf' in files:
    print('Warning: combined.pdf already exists, will be overwritten.')

do_continue = input('Continue? (y/n)')
while do_continue.strip().lower() != 'y':
    if do_continue.strip().lower() == 'n':
        exit()
    do_continue = input('Continue? (y/n)')

writer = pypdf.PdfWriter()


def is_sub(s1, s2):
    s1 = s1.strip().replace('\r', '').replace(' ', '')
    s2 = s2.replace('\n', '').replace('\r', '').replace(' ', '')
    
    for s in s1.split('\n'):
        if s not in s2:
            return False
        s2 = s2.replace(s, '', 1)

    return True


for pdf_file in pdf_files:
    f = open(pdf_file, 'rb')
    reader = pypdf.PdfReader(f)

    pages = []
    label = None
    last_page = None
    for i in range(len(reader.pages)):
        # It's the same page
        if label == reader.page_labels[i]:
            # Check texts
            if not is_sub(last_page.extract_text(), reader.pages[i].extract_text()):
                print(f'Conflict: {pdf_file} pages {i} and {i + 1}')
                pages.append(i)
            # Check images
            if last_page.images != reader.pages[i].images:
                print(f'Conflict: {pdf_file} pages {i} and {i + 1}')
                pages.append(i)

            pages[-1] = i
            last_page = reader.pages[i]
        # It's a new page
        else:
            pages.append(i)
            last_page = reader.pages[i]
            label = reader.page_labels[i]

    writer.append(fileobj=f, pages=pages)

with open('combined.pdf', 'wb') as f:
    writer.write(f)
