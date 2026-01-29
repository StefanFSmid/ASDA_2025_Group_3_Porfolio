import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    calc = 1 + 3
    print(calc)
    return


@app.cell
def _():
    markdown = 'text'
    markdown
    return


if __name__ == "__main__":
    app.run()
