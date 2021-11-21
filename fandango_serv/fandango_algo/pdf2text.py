from mytools.infer.predict_system import *


def reg_it(c, prefix):
    output = pdf2img2rec(c, prefix)
    demo(output)


if __name__ == '__main__':
    pdf = r"./fandango_algo/pdf/pdf_test/test1.pdf"
    with open(pdf, "rb") as f:
        c = f.read()
    reg_it(c, "./fandango_algo/")
    # reg_it(pdf,"")
    pass
