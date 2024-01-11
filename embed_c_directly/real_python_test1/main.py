import fputs

def test_copy_data():
    content_to_copy = "Real Python!"
    bytes_copied = fputs.fputs(content_to_copy, 'test_write.txt')

    with open('test_write.txt', 'r') as f:
        content_copied = f.read()

    assert content_copied == content_to_copy

if __name__ == "__main__":
    test_copy_data()
    print("Everything passed")
