app "hello"
    packages { pf: "cli" }
    imports [pf.Stdout]
    provides [main] to pf

main = Stdout.line "Hello, World!"
