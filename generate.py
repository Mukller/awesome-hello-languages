#!/usr/bin/env python3
"""Generate a "Hello, World!" program for every language in the catalog.

Each entry maps a language name to (relative_path, source_code). Running this
script (re)creates the files under ``languages/`` and prints a summary.
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "languages"

# name -> (path relative to languages/, source)
PROGRAMS: dict[str, tuple[str, str]] = {
    "C": ("c/hello.c",
        '#include <stdio.h>\n\nint main(void) {\n    printf("Hello, World!\\n");\n    return 0;\n}\n'),
    "C++": ("cpp/hello.cpp",
        '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n}\n'),
    "C#": ("csharp/Hello.cs",
        'using System;\n\nclass Hello {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}\n'),
    "Objective-C": ("objc/hello.m",
        '#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSLog(@"Hello, World!");\n    }\n}\n'),
    "Java": ("java/Hello.java",
        'public class Hello {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}\n'),
    "Kotlin": ("kotlin/hello.kt",
        'fun main() {\n    println("Hello, World!")\n}\n'),
    "Scala": ("scala/hello.scala",
        '@main def hello(): Unit = println("Hello, World!")\n'),
    "Groovy": ("groovy/hello.groovy", 'println "Hello, World!"\n'),
    "Clojure": ("clojure/hello.clj", '(println "Hello, World!")\n'),
    "Go": ("go/hello.go",
        'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}\n'),
    "Rust": ("rust/hello.rs", 'fn main() {\n    println!("Hello, World!");\n}\n'),
    "Swift": ("swift/hello.swift", 'print("Hello, World!")\n'),
    "Zig": ("zig/hello.zig",
        'const std = @import("std");\n\npub fn main() void {\n    std.debug.print("Hello, World!\\n", .{});\n}\n'),
    "D": ("d/hello.d",
        'import std.stdio;\n\nvoid main() {\n    writeln("Hello, World!");\n}\n'),
    "Nim": ("nim/hello.nim", 'echo "Hello, World!"\n'),
    "Crystal": ("crystal/hello.cr", 'puts "Hello, World!"\n'),
    "V": ("v/hello.v", 'fn main() {\n    println("Hello, World!")\n}\n'),
    "Python": ("python/hello.py", 'print("Hello, World!")\n'),
    "Ruby": ("ruby/hello.rb", 'puts "Hello, World!"\n'),
    "Perl": ("perl/hello.pl", 'print "Hello, World!\\n";\n'),
    "PHP": ("php/hello.php", '<?php\necho "Hello, World!\\n";\n'),
    "Lua": ("lua/hello.lua", 'print("Hello, World!")\n'),
    "JavaScript": ("javascript/hello.js", 'console.log("Hello, World!");\n'),
    "TypeScript": ("typescript/hello.ts", 'console.log("Hello, World!");\n'),
    "CoffeeScript": ("coffeescript/hello.coffee", 'console.log "Hello, World!"\n'),
    "Dart": ("dart/hello.dart", 'void main() {\n  print("Hello, World!");\n}\n'),
    "Elixir": ("elixir/hello.exs", 'IO.puts("Hello, World!")\n'),
    "Erlang": ("erlang/hello.erl",
        '-module(hello).\n-export([start/0]).\n\nstart() ->\n    io:format("Hello, World!~n").\n'),
    "Haskell": ("haskell/hello.hs", 'main :: IO ()\nmain = putStrLn "Hello, World!"\n'),
    "OCaml": ("ocaml/hello.ml", 'let () = print_endline "Hello, World!"\n'),
    "F#": ("fsharp/hello.fsx", 'printfn "Hello, World!"\n'),
    "Elm": ("elm/Hello.elm",
        'module Hello exposing (main)\n\nimport Html exposing (text)\n\nmain =\n    text "Hello, World!"\n'),
    "PureScript": ("purescript/Hello.purs",
        'module Main where\n\nimport Effect.Console (log)\n\nmain = log "Hello, World!"\n'),
    "Racket": ("racket/hello.rkt", '#lang racket\n(displayln "Hello, World!")\n'),
    "Scheme": ("scheme/hello.scm", '(display "Hello, World!")\n(newline)\n'),
    "Common Lisp": ("commonlisp/hello.lisp", '(format t "Hello, World!~%")\n'),
    "Fortran": ("fortran/hello.f90",
        'program hello\n    print *, "Hello, World!"\nend program hello\n'),
    "COBOL": ("cobol/hello.cob",
        '       IDENTIFICATION DIVISION.\n       PROGRAM-ID. HELLO.\n       PROCEDURE DIVISION.\n           DISPLAY "Hello, World!".\n           STOP RUN.\n'),
    "Pascal": ("pascal/hello.pas",
        'program Hello;\nbegin\n  writeln(\'Hello, World!\');\nend.\n'),
    "Ada": ("ada/hello.adb",
        'with Ada.Text_IO; use Ada.Text_IO;\n\nprocedure Hello is\nbegin\n   Put_Line("Hello, World!");\nend Hello;\n'),
    "Julia": ("julia/hello.jl", 'println("Hello, World!")\n'),
    "R": ("r/hello.R", 'cat("Hello, World!\\n")\n'),
    "MATLAB": ("matlab/hello.m", 'disp("Hello, World!")\n'),
    "Tcl": ("tcl/hello.tcl", 'puts "Hello, World!"\n'),
    "Bash": ("bash/hello.sh", '#!/usr/bin/env bash\necho "Hello, World!"\n'),
    "PowerShell": ("powershell/hello.ps1", 'Write-Output "Hello, World!"\n'),
    "Batch": ("batch/hello.bat", '@echo off\necho Hello, World!\n'),
    "AWK": ("awk/hello.awk", 'BEGIN { print "Hello, World!" }\n'),
    "sed": ("sed/hello.sed", 's/.*/Hello, World!/\n'),
    "Vimscript": ("vimscript/hello.vim", 'echo "Hello, World!"\n'),
    "SQL": ("sql/hello.sql", "SELECT 'Hello, World!' AS greeting;\n"),
    "Assembly (x86-64)": ("assembly/hello.asm",
        'section .data\n    msg db "Hello, World!", 10\n    len equ $ - msg\n\nsection .text\n    global _start\n_start:\n    mov rax, 1\n    mov rdi, 1\n    mov rsi, msg\n    mov rdx, len\n    syscall\n    mov rax, 60\n    xor rdi, rdi\n    syscall\n'),
    "Brainfuck": ("brainfuck/hello.bf",
        '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.\n'),
    "Smalltalk": ("smalltalk/hello.st", "Transcript showCr: 'Hello, World!'.\n"),
    "Prolog": ("prolog/hello.pl",
        ':- initialization(main).\n\nmain :- write(\'Hello, World!\'), nl.\n'),
    "Forth": ("forth/hello.fs", '." Hello, World!" CR\n'),
    "VHDL": ("vhdl/hello.vhd",
        'use std.textio.all;\n\nentity hello is end hello;\n\narchitecture sim of hello is\nbegin\n  process\n    variable l : line;\n  begin\n    write(l, string\'("Hello, World!"));\n    writeline(output, l);\n    wait;\n  end process;\nend sim;\n'),
    "Verilog": ("verilog/hello.v",
        'module hello;\n  initial begin\n    $display("Hello, World!");\n  end\nendmodule\n'),
    "Haxe": ("haxe/Hello.hx",
        'class Hello {\n    static function main() {\n        trace("Hello, World!");\n    }\n}\n'),
    "Vala": ("vala/hello.vala",
        'void main() {\n    print("Hello, World!\\n");\n}\n'),
    "Solidity": ("solidity/Hello.sol",
        '// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\n\ncontract Hello {\n    function greet() public pure returns (string memory) {\n        return "Hello, World!";\n    }\n}\n'),
    "ABAP": ("abap/hello.abap", "WRITE 'Hello, World!'.\n"),
    "Eiffel": ("eiffel/hello.e",
        'class HELLO\ncreate\n    make\nfeature\n    make\n        do\n            print("Hello, World!%N")\n        end\nend\n'),
    "Pony": ("pony/hello.pony",
        'actor Main\n  new create(env: Env) =>\n    env.out.print("Hello, World!")\n'),
    "Odin": ("odin/hello.odin",
        'package main\n\nimport "core:fmt"\n\nmain :: proc() {\n    fmt.println("Hello, World!")\n}\n'),
    "Gleam": ("gleam/hello.gleam",
        'import gleam/io\n\npub fn main() {\n  io.println("Hello, World!")\n}\n'),
    "ReScript": ("rescript/hello.res", 'Js.log("Hello, World!")\n'),
    "Wren": ("wren/hello.wren", 'System.print("Hello, World!")\n'),
    "Janet": ("janet/hello.janet", '(print "Hello, World!")\n'),
    "Hare": ("hare/hello.ha",
        'use fmt;\n\nexport fn main() void = {\n    fmt::println("Hello, World!")!;\n};\n'),
    "APL": ("apl/hello.apl", "'Hello, World!'\n"),
    "J": ("j/hello.ijs", "echo 'Hello, World!'\n"),
    "Raku": ("raku/hello.raku", 'say "Hello, World!";\n'),
    "Io": ("io/hello.io", '"Hello, World!" println\n'),
    "Rebol": ("rebol/hello.r", 'print "Hello, World!"\n'),
    "PostScript": ("postscript/hello.ps",
        '%!PS\n/Courier findfont 24 scalefont setfont\n72 700 moveto\n(Hello, World!) show\nshowpage\n'),
    "Logo": ("logo/hello.logo", 'print [Hello, World!]\n'),
    "Befunge": ("befunge/hello.bf", '"!dlroW ,olleH">:#,_@\n'),
    "Dafny": ("dafny/hello.dfy",
        'method Main() {\n    print "Hello, World!\\n";\n}\n'),
    "Chapel": ("chapel/hello.chpl", 'writeln("Hello, World!");\n'),
    "Mojo": ("mojo/hello.mojo",
        'fn main():\n    print("Hello, World!")\n'),
}

# Markup / data / config "hello worlds" for breadth.
MARKUP: dict[str, tuple[str, str]] = {
    "HTML": ("html/hello.html",
        '<!DOCTYPE html>\n<html>\n<body>\n  <p>Hello, World!</p>\n</body>\n</html>\n'),
    "Markdown": ("markdown/hello.md", '# Hello, World!\n'),
    "YAML": ("yaml/hello.yaml", 'greeting: "Hello, World!"\n'),
    "JSON": ("json/hello.json", '{\n  "greeting": "Hello, World!"\n}\n'),
    "TOML": ("toml/hello.toml", 'greeting = "Hello, World!"\n'),
    "XML": ("xml/hello.xml", '<?xml version="1.0"?>\n<greeting>Hello, World!</greeting>\n'),
    "CSS": ("css/hello.css",
        'body::before {\n  content: "Hello, World!";\n}\n'),
    "LaTeX": ("latex/hello.tex",
        '\\documentclass{article}\n\\begin{document}\nHello, World!\n\\end{document}\n'),
    "Makefile": ("makefile/Makefile",
        'all:\n\t@echo "Hello, World!"\n'),
}


def main() -> None:
    all_programs = {**PROGRAMS, **MARKUP}
    written = 0
    for name, (rel, src) in sorted(all_programs.items()):
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src, encoding="utf-8")
        written += 1
    print(f"Wrote {written} Hello World programs to {OUT}")
    print(f"Languages: {len(PROGRAMS)} | Markup/data formats: {len(MARKUP)}")


if __name__ == "__main__":
    main()
