from distutils.core import setup, Extension

def main():
    setup(name="fputs",
          version="1.0.0",
          description="Python interface for the fputs C library function",
          author="rv43",
          author_email="rv43@cornell.com",
          ext_modules=[Extension("fputs", ["fputs_wrapper.c"])])

if __name__ == "__main__":
    main()
