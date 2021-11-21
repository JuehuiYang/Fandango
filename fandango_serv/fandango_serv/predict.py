from fandango_algo.tools.infer.predict_system import pdf2img2rec, demo

if __name__ == "__main__":
    pdf = r"D:\IdeaProjects\Fandango\fandango_serv\test1.pdf"
    with open(pdf, "rb") as f:
        c = f.read()
    output = pdf2img2rec(c)
    demo(output)
