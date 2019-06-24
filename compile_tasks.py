import os
path = './examples/'

print('PROCESSING...')
for file_name in os.listdir(path):

    dot_pos = file_name.find('.')

    if dot_pos < 0:
        continue

    ext = file_name[dot_pos+1:]
    if ext != 'lnt':
        continue

    file_name = file_name[:dot_pos]

    input_file_name = '{}.{}'.format(path+file_name, ext)
    python_file_name = '{}.py'.format(path+file_name)

    os.system('python lant.py {} > {}'.format(
        input_file_name,
        python_file_name
    ))

    print(f"File {input_file_name} is compiled")

print('DONE')

