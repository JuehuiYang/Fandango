import fandango_algo as falg
from fandango_algo.mytools.infer import predict_system
from fandango_algo.pdf2text import reg_it

if __name__ == '__main__':
    # predict_system.
    # pdf="./fandango_algo/pdf/pdf_test/test1.pdf"
    pdf = r"./fandango_algo/pdf/pdf_test/test1.pdf"
    with open(pdf, "rb") as f:
        c = f.read()
    reg_it(c, "./fandango_algo/")
    pass
