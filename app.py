from socketify import App

app = App()

app.get("/", lambda res, req: res.end("Hello, world!"))
app.listen(3000, lambda config: print(f"LISTENING ON http://localhost:{config.port}"))

app.run()