def handle_uploaded_file(f):
    with open('/home/rane/ashu/Files/test.txt', 'wb+') as destination:
        print('in handle upload')
        for chunk in f.chunks():
            destination.write(chunk)
