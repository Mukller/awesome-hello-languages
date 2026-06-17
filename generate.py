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

# ---------------------------------------------------------------------------
# Expanded catalog: many more programming languages.
# ---------------------------------------------------------------------------
EXTRA_PROGRAMS: dict[str, tuple[str, str]] = {
    # --- Shells ---
    "Fish": ("fish/hello.fish", 'echo "Hello, World!"\n'),
    "Zsh": ("zsh/hello.zsh", 'echo "Hello, World!"\n'),
    "Ksh": ("ksh/hello.ksh", 'print "Hello, World!"\n'),
    "Csh": ("csh/hello.csh", 'echo "Hello, World!"\n'),
    "Tcsh": ("tcsh/hello.tcsh", 'echo "Hello, World!"\n'),
    "Nushell": ("nushell/hello.nu", 'print "Hello, World!"\n'),
    "Elvish": ("elvish/hello.elv", 'echo "Hello, World!"\n'),
    "Xonsh": ("xonsh/hello.xsh", 'print("Hello, World!")\n'),
    # --- Lisps / Schemes ---
    "Emacs Lisp": ("emacslisp/hello.el", '(princ "Hello, World!\\n")\n'),
    "Fennel": ("fennel/hello.fnl", '(print "Hello, World!")\n'),
    "Hy": ("hy/hello.hy", '(print "Hello, World!")\n'),
    "PicoLisp": ("picolisp/hello.l", '(prinl "Hello, World!")\n'),
    "newLISP": ("newlisp/hello.lsp", '(println "Hello, World!")\n'),
    "Carp": ("carp/hello.carp", '(defn main [] (println "Hello, World!"))\n'),
    "Guile": ("guile/hello.scm", '(display "Hello, World!")(newline)\n'),
    # --- ML / functional ---
    "Standard ML": ("sml/hello.sml", 'print "Hello, World!\\n";\n'),
    "Reason": ("reason/hello.re", 'print_string("Hello, World!\\n");\n'),
    "Idris": ("idris/hello.idr", 'main : IO ()\nmain = putStrLn "Hello, World!"\n'),
    "Lean": ("lean/hello.lean", 'def main : IO Unit := IO.println "Hello, World!"\n'),
    "Mercury": ("mercury/hello.m",
        ':- module hello.\n:- interface.\n:- import_module io.\n:- pred main(io::di, io::uo) is det.\n:- implementation.\nmain(!IO) :- io.write_string("Hello, World!\\n", !IO).\n'),
    "Frege": ("frege/Hello.fr", 'module Hello where\n\nmain = println "Hello, World!"\n'),
    "Koka": ("koka/hello.kk", 'fun main()\n  println("Hello, World!")\n'),
    "Grain": ("grain/hello.gr", 'print("Hello, World!")\n'),
    "Roc": ("roc/hello.roc",
        'app "hello"\n    packages {{ pf: "cli" }}\n    imports [pf.Stdout]\n    provides [main] to pf\n\nmain = Stdout.line "Hello, World!"\n'.replace("{{", "{").replace("}}", "}")),
    "Unison": ("unison/hello.u", 'main : \'{IO, Exception} ()\nmain _ = printLine "Hello, World!"\n'),
    # --- JVM / .NET extras ---
    "Fantom": ("fantom/hello.fan",
        'class Hello {\n  static Void main() {\n    echo("Hello, World!")\n  }\n}\n'),
    "Ceylon": ("ceylon/hello.ceylon", 'shared void run() {\n    print("Hello, World!");\n}\n'),
    "Xtend": ("xtend/Hello.xtend",
        'class Hello {\n  def static void main(String[] args) {\n    println("Hello, World!")\n  }\n}\n'),
    "Visual Basic .NET": ("vbnet/Hello.vb",
        'Module Hello\n    Sub Main()\n        Console.WriteLine("Hello, World!")\n    End Sub\nEnd Module\n'),
    "VBScript": ("vbscript/hello.vbs", 'WScript.Echo "Hello, World!"\n'),
    "FreeBASIC": ("freebasic/hello.bas", 'print "Hello, World!"\n'),
    "QBasic": ("qbasic/hello.bas", 'PRINT "Hello, World!"\n'),
    "Boo": ("boo/hello.boo", 'print "Hello, World!"\n'),
    "Nemerle": ("nemerle/hello.n", 'System.Console.WriteLine("Hello, World!");\n'),
    "Genie": ("genie/hello.gs", 'init\n    print "Hello, World!"\n'),
    "Hack": ("hack/hello.hack",
        '<?hh\n\nfunction main(): void {\n  echo "Hello, World!\\n";\n}\n'),
    "Apex": ("apex/Hello.cls",
        'public class Hello {\n    public static void say() {\n        System.debug("Hello, World!");\n    }\n}\n'),
    # --- Scripting / game ---
    "GDScript": ("gdscript/hello.gd",
        'extends Node\n\nfunc _ready():\n    print("Hello, World!")\n'),
    "AngelScript": ("angelscript/hello.as", 'void main() {\n    print("Hello, World!\\n");\n}\n'),
    "ActionScript": ("actionscript/hello.as", 'trace("Hello, World!");\n'),
    "Squirrel": ("squirrel/hello.nut", 'print("Hello, World!\\n")\n'),
    "GML": ("gml/hello.gml", 'show_message("Hello, World!");\n'),
    "Pawn": ("pawn/hello.pwn", 'main() {\n    print("Hello, World!");\n}\n'),
    "AutoHotkey": ("autohotkey/hello.ahk", 'MsgBox, Hello, World!\n'),
    "AutoIt": ("autoit/hello.au3", 'ConsoleWrite("Hello, World!" & @CRLF)\n'),
    "Inform 7": ("inform7/hello.ni",
        'The greeting room is a room.\n\nWhen play begins: say "Hello, World!".\n'),
    # --- Modern systems ---
    "C3": ("c3/hello.c3",
        'import std::io;\n\nfn void main() {\n    io::printn("Hello, World!");\n}\n'),
    "Carbon": ("carbon/hello.carbon",
        'package sample api;\n\nfn Main() -> i32 {\n  Core.Print("Hello, World!");\n  return 0;\n}\n'),
    "Seed7": ("seed7/hello.sd7",
        '$ include "seed7_05.s7i";\n\nconst proc: main is func\n  begin\n    writeln("Hello, World!");\n  end func;\n'),
    "Ballerina": ("ballerina/hello.bal",
        'import ballerina/io;\n\npublic function main() {\n    io:println("Hello, World!");\n}\n'),
    "Inko": ("inko/hello.inko",
        'import std.stdio (STDOUT)\n\nclass async Main {\n  fn async main {\n    STDOUT.new.print("Hello, World!")\n  }\n}\n'),
    "Cobra": ("cobra/hello.cobra",
        'class Hello\n    def main\n        print "Hello, World!"\n'),
    # --- Classic / legacy ---
    "Modula-2": ("modula2/hello.mod",
        'MODULE Hello;\nFROM STextIO IMPORT WriteString, WriteLn;\nBEGIN\n  WriteString("Hello, World!");\n  WriteLn;\nEND Hello.\n'),
    "Oberon": ("oberon/Hello.Mod",
        'MODULE Hello;\nIMPORT Out;\nBEGIN\n  Out.String("Hello, World!");\n  Out.Ln\nEND Hello.\n'),
    "Algol 68": ("algol68/hello.a68", 'print(("Hello, World!", new line))\n'),
    "BCPL": ("bcpl/hello.b",
        'GET "libhdr"\n\nLET start() = VALOF\n$( writes("Hello, World!*N")\n   RESULTIS 0\n$)\n'),
    "PL/I": ("pli/hello.pli",
        'Hello: procedure options (main);\n  put list ("Hello, World!");\nend Hello;\n'),
    "Simula": ("simula/hello.sim",
        'BEGIN\n  OutText("Hello, World!");\n  OutImage;\nEND;\n'),
    "REXX": ("rexx/hello.rexx", 'say "Hello, World!"\n'),
    "SNOBOL": ("snobol/hello.sno", ' OUTPUT = "Hello, World!"\nEND\n'),
    "Icon": ("icon/hello.icn", 'procedure main()\n    write("Hello, World!")\nend\n'),
    "Unicon": ("unicon/hello.ucn", 'procedure main()\n    write("Hello, World!")\nend\n'),
    "Pike": ("pike/hello.pike",
        'int main() {\n    write("Hello, World!\\n");\n    return 0;\n}\n'),
    "Euphoria": ("euphoria/hello.ex", 'puts(1, "Hello, World!\\n")\n'),
    "Ring": ("ring/hello.ring", 'see "Hello, World!" + nl\n'),
    "Red": ("red/hello.red", 'Red [] print "Hello, World!"\n'),
    # --- Math / scientific ---
    "Octave": ("octave/hello.m", 'disp("Hello, World!")\n'),
    "Scilab": ("scilab/hello.sci", 'disp("Hello, World!")\n'),
    "Maxima": ("maxima/hello.mac", 'print("Hello, World!")$\n'),
    "GAP": ("gap/hello.g", 'Print("Hello, World!\\n");\n'),
    "Wolfram": ("wolfram/hello.wl", 'Print["Hello, World!"]\n'),
    "Stata": ("stata/hello.do", 'display "Hello, World!"\n'),
    "SAS": ("sas/hello.sas", 'data _null_;\n  put "Hello, World!";\nrun;\n'),
    "Gnuplot": ("gnuplot/hello.gp", 'print "Hello, World!"\n'),
    "Maple": ("maple/hello.mpl", 'printf("Hello, World!\\n");\n'),
    "Q (kdb+)": ("q/hello.q", 'show "Hello, World!"\n'),
    "K": ("k/hello.k", '`0:"Hello, World!\\n"\n'),
    "BQN": ("bqn/hello.bqn", '•Out "Hello, World!"\n'),
    "Uiua": ("uiua/hello.ua", '&p "Hello, World!"\n'),
    "Frink": ("frink/hello.frink", 'println["Hello, World!"]\n'),
    "bc": ("bc/hello.bc", 'print "Hello, World!\\n"\n'),
    "dc": ("dc/hello.dc", '[Hello, World!]p\n'),
    "m4": ("m4/hello.m4", "Hello, World!\n"),
    # --- GPU / parallel ---
    "CUDA": ("cuda/hello.cu",
        '#include <cstdio>\n\n__global__ void hello() {\n    printf("Hello, World!\\n");\n}\n\nint main() {\n    hello<<<1, 1>>>();\n    cudaDeviceSynchronize();\n}\n'),
    "OpenCL": ("opencl/hello.cl",
        '__kernel void hello() {\n    printf("Hello, World!\\n");\n}\n'),
    # --- DB dialects ---
    "PL/pgSQL": ("plpgsql/hello.sql",
        "DO $$\nBEGIN\n  RAISE NOTICE 'Hello, World!';\nEND $$;\n"),
    "PL/SQL": ("plsql/hello.sql",
        "BEGIN\n  DBMS_OUTPUT.PUT_LINE('Hello, World!');\nEND;\n/\n"),
    "T-SQL": ("tsql/hello.sql", "PRINT 'Hello, World!';\n"),
    # --- Hardware / build ---
    "SystemVerilog": ("systemverilog/hello.sv",
        'module hello;\n  initial $display("Hello, World!");\nendmodule\n'),
    "CMake": ("cmake/hello.cmake", 'message("Hello, World!")\n'),
    "Meson": ("meson/meson.build", "project('hello', 'c')\nmessage('Hello, World!')\n"),
    "Just": ("just/justfile", 'hello:\n    @echo "Hello, World!"\n'),
    "Dockerfile": ("dockerfile/Dockerfile",
        'FROM alpine\nCMD ["echo", "Hello, World!"]\n'),
    "Nix": ("nix/hello.nix", '"Hello, World!"\n'),
    "Terraform": ("terraform/hello.tf",
        'output "greeting" {\n  value = "Hello, World!"\n}\n'),
    "Starlark": ("starlark/hello.star", 'print("Hello, World!")\n'),
    # --- Creative coding ---
    "Processing": ("processing/hello.pde",
        'void setup() {\n  println("Hello, World!");\n}\n'),
    "Arduino": ("arduino/hello.ino",
        'void setup() {\n  Serial.begin(9600);\n  Serial.println("Hello, World!");\n}\n\nvoid loop() {}\n'),
    "OpenSCAD": ("openscad/hello.scad", 'echo("Hello, World!");\n'),
    "Cython": ("cython/hello.pyx", 'print("Hello, World!")\n'),
    "ColdFusion": ("coldfusion/hello.cfm", '<cfoutput>Hello, World!</cfoutput>\n'),
    # --- Esoteric ---
    "LOLCODE": ("lolcode/hello.lol",
        'HAI 1.2\nVISIBLE "Hello, World!"\nKTHXBYE\n'),
    "Rockstar": ("rockstar/hello.rock", 'Say "Hello, World!"\n'),
    "ArnoldC": ("arnoldc/hello.arnoldc",
        'IT\'S SHOWTIME\nTALK TO THE HAND "Hello, World!"\nYOU HAVE BEEN TERMINATED\n'),
    "Emojicode": ("emojicode/hello.emojic",
        '\U0001f3c1 \U0001f346\n  \U0001f600 \U0001f524Hello, World!\U0001f524❗️\n\U0001f349\n'),
    "GolfScript": ("golfscript/hello.gs", '"Hello, World!"\n'),
    "CJam": ("cjam/hello.cjam", '"Hello, World!"\n'),
    "WebAssembly (WAT)": ("wat/hello.wat",
        '(module\n  (import "wasi_snapshot_preview1" "fd_write"\n    (func $fd_write (param i32 i32 i32 i32) (result i32)))\n  (memory 1)\n  (export "memory" (memory 0))\n  (data (i32.const 8) "Hello, World!\\n")\n  (func $main (export "_start")\n    (i32.store (i32.const 0) (i32.const 8))\n    (i32.store (i32.const 4) (i32.const 14))\n    (call $fd_write (i32.const 1) (i32.const 0) (i32.const 1) (i32.const 20))\n    drop))\n'),
}

# ---------------------------------------------------------------------------
# Expanded catalog: more markup / data / config formats.
# ---------------------------------------------------------------------------
EXTRA_MARKUP: dict[str, tuple[str, str]] = {
    "SVG": ("svg/hello.svg",
        '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="40">\n  <text x="10" y="25">Hello, World!</text>\n</svg>\n'),
    "reStructuredText": ("rst/hello.rst", 'Hello, World!\n=============\n'),
    "AsciiDoc": ("asciidoc/hello.adoc", '= Hello, World!\n'),
    "Org-mode": ("org/hello.org", '* Hello, World!\n'),
    "INI": ("ini/hello.ini", '[greeting]\nmessage = Hello, World!\n'),
    "CSV": ("csv/hello.csv", 'greeting\n"Hello, World!"\n'),
    "Java Properties": ("properties/hello.properties", 'greeting=Hello, World!\n'),
    "HOCON": ("hocon/hello.conf", 'greeting = "Hello, World!"\n'),
    "EDN": ("edn/hello.edn", '{:greeting "Hello, World!"}\n'),
    "Dhall": ("dhall/hello.dhall", '"Hello, World!"\n'),
    "Jsonnet": ("jsonnet/hello.jsonnet", '{ greeting: "Hello, World!" }\n'),
    "CUE": ("cue/hello.cue", 'greeting: "Hello, World!"\n'),
    "Nickel": ("nickel/hello.ncl", '"Hello, World!"\n'),
    "GraphQL": ("graphql/hello.graphql", 'type Query {\n  greeting: String\n}\n'),
    "Protocol Buffers": ("protobuf/hello.proto",
        'syntax = "proto3";\n\nmessage Greeting {\n  string text = 1;\n}\n'),
    "Apache Thrift": ("thrift/hello.thrift",
        'struct Greeting {\n  1: string text\n}\n'),
}

PROGRAMS.update(EXTRA_PROGRAMS)
MARKUP.update(EXTRA_MARKUP)

# ---------------------------------------------------------------------------
# Third wave: more languages — functional/logic, blockchain, assembly/IR,
# UI DSLs, shaders, and esoteric.
# ---------------------------------------------------------------------------
EXTRA2_PROGRAMS: dict[str, tuple[str, str]] = {
    "Factor": ("factor/hello.factor", 'USING: io ;\n"Hello, World!" print\n'),
    "Joy": ("joy/hello.joy", '"Hello, World!" putchars.\n'),
    "Curry": ("curry/hello.curry", 'main = putStrLn "Hello, World!"\n'),
    "Clean": ("clean/hello.icl",
        'module hello\n\nStart :: String\nStart = "Hello, World!"\n'),
    "Oz": ("oz/hello.oz",
        'functor\nimport System\ndefine\n  {System.showInfo "Hello, World!"}\nend\n'),
    "ATS": ("ats/hello.dats", 'implement main0 () = print "Hello, World!\\n"\n'),
    "LFE": ("lfe/hello.lfe", '(io:format "Hello, World!~n")\n'),
    "Datalog": ("datalog/hello.dl", 'greeting("Hello, World!").\n'),
    "Nit": ("nit/hello.nit", 'print "Hello, World!"\n'),
    "Felix": ("felix/hello.flx", 'println "Hello, World!";\n'),
    "Onyx": ("onyx/hello.onyx",
        'use core {println}\n\nmain :: () {\n    println("Hello, World!");\n}\n'),
    "Beef": ("beef/hello.bf",
        'namespace Hello;\n\nclass Program {\n    public static void Main() {\n        System.Console.WriteLine("Hello, World!");\n    }\n}\n'),
    "Nial": ("nial/hello.ndf", 'write "Hello, World!"\n'),
    "PARI/GP": ("pari/hello.gp", 'print("Hello, World!")\n'),
    "SPSS": ("spss/hello.sps", 'ECHO "Hello, World!".\n'),
    "AppleScript": ("applescript/hello.applescript", 'log "Hello, World!"\n'),
    "Luau": ("luau/hello.luau", 'print("Hello, World!")\n'),
    # --- Blockchain / smart contracts ---
    "Vyper": ("vyper/hello.vy",
        '@external\n@view\ndef greet() -> String[16]:\n    return "Hello, World!"\n'),
    "Move": ("move/hello.move",
        'module hello::greeting {\n    use std::debug;\n    public fun say() {\n        debug::print(&b"Hello, World!");\n    }\n}\n'),
    "Clarity": ("clarity/hello.clar", '(print "Hello, World!")\n'),
    # --- UI DSLs ---
    "QML": ("qml/hello.qml",
        'import QtQuick 2.0\n\nText {\n    text: "Hello, World!"\n}\n'),
    "Slint": ("slint/hello.slint",
        'export component Hello {\n    Text { text: "Hello, World!"; }\n}\n'),
    # --- Assembly variants & IR ---
    "ARM Assembly": ("arm-asm/hello.s",
        '.data\nmsg: .ascii "Hello, World!\\n"\n.text\n.global _start\n_start:\n    mov r7, #4\n    mov r0, #1\n    ldr r1, =msg\n    mov r2, #14\n    swi 0\n    mov r7, #1\n    swi 0\n'),
    "MIPS Assembly": ("mips-asm/hello.s",
        '.data\nmsg: .asciiz "Hello, World!\\n"\n.text\nmain:\n    li $v0, 4\n    la $a0, msg\n    syscall\n    li $v0, 10\n    syscall\n'),
    "RISC-V Assembly": ("riscv-asm/hello.s",
        '.section .data\nmsg: .ascii "Hello, World!\\n"\n.section .text\n.globl _start\n_start:\n    li a7, 64\n    li a0, 1\n    la a1, msg\n    li a2, 14\n    ecall\n    li a7, 93\n    li a0, 0\n    ecall\n'),
    "LLVM IR": ("llvm-ir/hello.ll",
        '@.str = private constant [15 x i8] c"Hello, World!\\0A\\00"\n\ndeclare i32 @puts(i8*)\n\ndefine i32 @main() {\n  %s = getelementptr [15 x i8], [15 x i8]* @.str, i64 0, i64 0\n  call i32 @puts(i8* %s)\n  ret i32 0\n}\n'),
    # --- Shaders (greeting in source; output is a color) ---
    "GLSL": ("glsl/hello.frag",
        '#version 330 core\nout vec4 fragColor;\n// Hello, World!\nvoid main() {\n    fragColor = vec4(0.0, 1.0, 0.0, 1.0);\n}\n'),
    "HLSL": ("hlsl/hello.hlsl",
        '// Hello, World!\nfloat4 main() : SV_Target {\n    return float4(0.0, 1.0, 0.0, 1.0);\n}\n'),
    "WGSL": ("wgsl/hello.wgsl",
        '// Hello, World!\n@fragment\nfn main() -> @location(0) vec4<f32> {\n    return vec4<f32>(0.0, 1.0, 0.0, 1.0);\n}\n'),
    "Metal": ("metal/hello.metal",
        '#include <metal_stdlib>\nusing namespace metal;\n// Hello, World!\nfragment float4 hello() {\n    return float4(0.0, 1.0, 0.0, 1.0);\n}\n'),
    "POV-Ray": ("povray/hello.pov", '#debug "Hello, World!\\n"\n'),
}

EXTRA2_MARKUP: dict[str, tuple[str, str]] = {
    # --- Templating engines ---
    "Jinja2": ("jinja/hello.j2", '{{ "Hello, World!" }}\n'),
    "Handlebars": ("handlebars/hello.hbs", 'Hello, World!\n'),
    "Mustache": ("mustache/hello.mustache", 'Hello, World!\n'),
    "ERB": ("erb/hello.erb", '<%= "Hello, World!" %>\n'),
    "EJS": ("ejs/hello.ejs", '<%= "Hello, World!" %>\n'),
    "Pug": ("pug/hello.pug", 'p Hello, World!\n'),
    "Haml": ("haml/hello.haml", '%p Hello, World!\n'),
    "Slim": ("slim/hello.slim", 'p Hello, World!\n'),
    "Liquid": ("liquid/hello.liquid", '{{ "Hello, World!" }}\n'),
    "Twig": ("twig/hello.twig", '{{ "Hello, World!" }}\n'),
    # --- Schema / data ---
    "Cap'n Proto": ("capnproto/hello.capnp",
        '@0x934efea7f017fff0;\n\nstruct Greeting {\n  text @0 :Text;\n}\n'),
    "FlatBuffers": ("flatbuffers/hello.fbs",
        'table Greeting {\n  text:string;\n}\n\nroot_type Greeting;\n'),
    "Avro": ("avro/hello.avsc",
        '{\n  "type": "record",\n  "name": "Greeting",\n  "fields": [{"name": "text", "type": "string"}]\n}\n'),
    "KDL": ("kdl/hello.kdl", 'greeting "Hello, World!"\n'),
    "RON": ("ron/hello.ron", 'Greeting(\n    text: "Hello, World!",\n)\n'),
    "XAML": ("xaml/hello.xaml",
        '<TextBlock xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"\n           Text="Hello, World!" />\n'),
    "BibTeX": ("bibtex/hello.bib", '@misc{hello, title = {Hello, World!}}\n'),
    "Graphviz DOT": ("dot/hello.dot", 'digraph G {\n    "Hello, World!";\n}\n'),
    "PlantUML": ("plantuml/hello.puml",
        '@startuml\nAlice -> Bob : Hello, World!\n@enduml\n'),
    "Mermaid": ("mermaid/hello.mmd", 'graph TD\n    A[Hello, World!]\n'),
    "GitHub Actions": ("githubactions/hello.yml",
        'name: hello\non: push\njobs:\n  hello:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo "Hello, World!"\n'),
    "Ninja": ("ninja/build.ninja",
        'rule echo\n  command = echo "Hello, World!"\n\nbuild hello: echo\n'),
    "Gradle": ("gradle/build.gradle",
        'task hello {\n    doLast {\n        println "Hello, World!"\n    }\n}\n'),
}

PROGRAMS.update(EXTRA2_PROGRAMS)
MARKUP.update(EXTRA2_MARKUP)

# Ook! is a 1:1 transliteration of Brainfuck — derive it from the BF program
# so it is guaranteed correct rather than hand-typed.
_BF_TO_OOK = {
    ">": "Ook. Ook?", "<": "Ook? Ook.", "+": "Ook. Ook.", "-": "Ook! Ook!",
    ".": "Ook! Ook.", ",": "Ook. Ook!", "[": "Ook! Ook?", "]": "Ook? Ook!",
}
_bf_source = PROGRAMS["Brainfuck"][1]
PROGRAMS["Ook!"] = (
    "ook/hello.ook",
    " ".join(_BF_TO_OOK[c] for c in _bf_source if c in _BF_TO_OOK) + "\n",
)

# ---------------------------------------------------------------------------
# Fourth wave: still more languages and formats.
# ---------------------------------------------------------------------------
EXTRA3_PROGRAMS: dict[str, tuple[str, str]] = {
    # --- Object / prototype ---
    "Self": ("self/hello.self", "'Hello, World!' printLine.\n"),
    # --- Newer / niche general-purpose ---
    "ChaiScript": ("chaiscript/hello.chai", 'print("Hello, World!")\n'),
    "Gravity": ("gravity/hello.gravity",
        'func main() {\n    System.print("Hello, World!")\n}\n'),
    "Terra": ("terra/hello.t", 'print("Hello, World!")\n'),
    "MoonScript": ("moonscript/hello.moon", 'print "Hello, World!"\n'),
    "Jakt": ("jakt/hello.jakt", 'fn main() {\n    println("Hello, World!")\n}\n'),
    "Hylo": ("hylo/hello.hylo", 'public fun main() {\n  print("Hello, World!")\n}\n'),
    "Vale": ("vale/hello.vale",
        'exported func main() {\n  println("Hello, World!");\n}\n'),
    "Cyber": ("cyber/hello.cy", 'print "Hello, World!"\n'),
    # --- Legacy / business ---
    "Fortran 77": ("fortran77/hello.f",
        "      PROGRAM HELLO\n      PRINT *, 'Hello, World!'\n      END\n"),
    "Modula-3": ("modula3/Hello.m3",
        'MODULE Hello EXPORTS Main;\nIMPORT IO;\nBEGIN\n  IO.Put("Hello, World!\\n");\nEND Hello.\n'),
    "Delphi": ("delphi/hello.dpr",
        "program Hello;\nbegin\n  WriteLn('Hello, World!');\nend.\n"),
    "RPG": ("rpg/hello.rpgle", "**free\ndsply 'Hello, World!';\nreturn;\n"),
    "OpenEdge ABL": ("abl/hello.p", 'DISPLAY "Hello, World!".\n'),
    "FoxPro": ("foxpro/hello.prg", '? "Hello, World!"\n'),
    "IDL": ("idl/hello.pro", "print, 'Hello, World!'\n"),
    "Yorick": ("yorick/hello.i", 'write, "Hello, World!"\n'),
    "CLIST": ("clist/hello.clist", 'WRITE Hello, World!\n'),
    # --- Retro assembly ---
    "x86 (DOS)": ("x86-dos/hello.asm",
        'org 100h\n    mov ah, 9\n    mov dx, msg\n    int 21h\n    ret\nmsg db "Hello, World!$"\n'),
    "Z80 (CP/M)": ("z80-cpm/hello.asm",
        '    org 100h\n    ld de, msg\n    ld c, 9\n    call 5\n    ret\nmsg: db "Hello, World!$"\n'),
    # --- Query languages ---
    "SPARQL": ("sparql/hello.rq",
        'SELECT ("Hello, World!" AS ?greeting) WHERE {}\n'),
    "Cypher": ("cypher/hello.cypher", 'RETURN "Hello, World!" AS greeting\n'),
    "XQuery": ("xquery/hello.xq", '"Hello, World!"\n'),
    "XSLT": ("xslt/hello.xsl",
        '<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n  <xsl:template match="/">Hello, World!</xsl:template>\n</xsl:stylesheet>\n'),
    "jq": ("jq/hello.jq", '"Hello, World!"\n'),
    # --- Infrastructure ---
    "Puppet": ("puppet/hello.pp", "notify { 'Hello, World!': }\n"),
    "Bicep": ("bicep/hello.bicep", "output greeting string = 'Hello, World!'\n"),
    "Chef (Infra)": ("chef-infra/hello.rb", 'log "Hello, World!"\n'),
}

EXTRA3_MARKUP: dict[str, tuple[str, str]] = {
    # --- Stylesheets ---
    "SCSS": ("scss/hello.scss", 'body::before { content: "Hello, World!"; }\n'),
    "Less": ("less/hello.less", 'body::before { content: "Hello, World!"; }\n'),
    "Stylus": ("stylus/hello.styl", 'body::before\n  content "Hello, World!"\n'),
    # --- Document markup ---
    "Typst": ("typst/hello.typ", 'Hello, World!\n'),
    "Djot": ("djot/hello.dj", 'Hello, World!\n'),
    "Gemtext": ("gemtext/hello.gmi", '# Hello, World!\n'),
    "Troff": ("troff/hello.tr", '.PP\nHello, World!\n'),
    "Texinfo": ("texinfo/hello.texi",
        '\\input texinfo\n@settitle Hello\nHello, World!\n@bye\n'),
    "MDX": ("mdx/hello.mdx", '# Hello, World!\n'),
    "Textile": ("textile/hello.textile", 'h1. Hello, World!\n'),
    "MediaWiki": ("mediawiki/hello.wiki", "= Hello, World! =\n"),
    "POD": ("pod/hello.pod", '=pod\n\nHello, World!\n\n=cut\n'),
    "DocBook": ("docbook/hello.dbk",
        '<?xml version="1.0"?>\n<article><para>Hello, World!</para></article>\n'),
    # --- Data / interchange ---
    "vCard": ("vcard/hello.vcf",
        'BEGIN:VCARD\nVERSION:3.0\nFN:Hello, World!\nEND:VCARD\n'),
    "iCalendar": ("icalendar/hello.ics",
        'BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nSUMMARY:Hello, World!\nEND:VEVENT\nEND:VCALENDAR\n'),
    "TSV": ("tsv/hello.tsv", 'greeting\tvalue\nmessage\tHello, World!\n'),
    "dotenv": ("dotenv/hello.env", 'GREETING="Hello, World!"\n'),
    "Pkl": ("pkl/hello.pkl", 'greeting = "Hello, World!"\n'),
    # --- Infra config ---
    "Ansible": ("ansible/hello.yml",
        '- hosts: localhost\n  tasks:\n    - debug:\n        msg: "Hello, World!"\n'),
    "Earthfile": ("earthfile/Earthfile",
        'VERSION 0.7\nhello:\n    RUN echo "Hello, World!"\n'),
}

PROGRAMS.update(EXTRA3_PROGRAMS)
MARKUP.update(EXTRA3_MARKUP)

# Spoon and Whitespace are derived programmatically so they are byte-correct.
# Spoon is a 1:1 binary re-encoding of Brainfuck.
_BF_TO_SPOON = {
    "+": "1", "-": "000", ">": "010", "<": "011",
    "[": "00100", "]": "0011", ".": "001010", ",": "0010110",
}
PROGRAMS["Spoon"] = (
    "spoon/hello.sp",
    "".join(_BF_TO_SPOON[c] for c in _bf_source if c in _BF_TO_SPOON) + "\n",
)


def _whitespace(text: str) -> str:
    """Emit a Whitespace program that prints ``text`` (space=0, tab=1, LF=cmd)."""
    out: list[str] = []
    for ch in text:
        bits = "".join("\t" if b == "1" else " " for b in bin(ord(ch))[2:])
        out.append("  " + " " + bits + "\n")  # IMP=SS push, positive sign, bits, LF
        out.append("\t\n  ")                   # IMP=TL, SS = output character
    out.append("\n\n\n")                       # end program
    return "".join(out)


PROGRAMS["Whitespace"] = ("whitespace/hello.ws", _whitespace("Hello, World!\n"))

# ---------------------------------------------------------------------------
# Fifth wave: web/template engines, engine scripting, music, proof/logic,
# retro BASICs, more shells, and data schemas.
# ---------------------------------------------------------------------------
EXTRA4_PROGRAMS: dict[str, tuple[str, str]] = {
    # --- Automation / scripting ---
    "Expect": ("expect/hello.exp", 'send_user "Hello, World!\\n"\n'),
    "HyperTalk": ("hypertalk/hello.ht", 'put "Hello, World!"\n'),
    "NSIS": ("nsis/hello.nsi",
        'OutFile "hello.exe"\nSection\n  MessageBox MB_OK "Hello, World!"\nSectionEnd\n'),
    # --- Shells ---
    "OSH (Oils)": ("osh/hello.osh", 'echo "Hello, World!"\n'),
    "Murex": ("murex/hello.mx", 'out "Hello, World!"\n'),
    "Ion": ("ion/hello.ion", 'echo "Hello, World!"\n'),
    "rc (Plan 9)": ("rc/hello.rc", 'echo Hello, World!\n'),
    # --- Interactive fiction / education ---
    "Ren'Py": ("renpy/hello.rpy", 'label start:\n    "Hello, World!"\n'),
    "Inform 6": ("inform6/hello.inf", '[ Main; print "Hello, World!^"; ];\n'),
    "NetLogo": ("netlogo/hello.nlogo",
        'to hello\n  print "Hello, World!"\nend\n'),
    # --- Game engine scripting ---
    "UnrealScript": ("unrealscript/Hello.uc",
        'class Hello extends Object;\n\nfunction Hello() {\n    `log("Hello, World!");\n}\n'),
    "Papyrus": ("papyrus/Hello.psc",
        'Scriptname Hello\n\nFunction Say()\n    Debug.Trace("Hello, World!")\nEndFunction\n'),
    "QuakeC": ("quakec/hello.qc",
        'void() main = {\n    print("Hello, World!\\n");\n};\n'),
    # --- Music / creative coding ---
    "ChucK": ("chuck/hello.ck", '<<< "Hello, World!" >>>;\n'),
    "SuperCollider": ("supercollider/hello.scd", '"Hello, World!".postln;\n'),
    "LilyPond": ("lilypond/hello.ly", '\\markup { "Hello, World!" }\n'),
    # --- Proof / logic / constraints ---
    "TLA+": ("tlaplus/hello.tla",
        '---- MODULE hello ----\nEXTENDS TLC\nASSUME PrintT("Hello, World!")\n====\n'),
    "Picat": ("picat/hello.pi", 'main => println("Hello, World!").\n'),
    "MiniZinc": ("minizinc/hello.mzn", 'output ["Hello, World!"];\n'),
    "SMT-LIB": ("smtlib/hello.smt2", '(echo "Hello, World!")\n'),
    "ACL2": ("acl2/hello.lisp", '(cw "Hello, World!~%")\n'),
    # --- Scientific / CAS ---
    "Magma": ("magma/hello.magma", '"Hello, World!";\n'),
    "Singular": ("singular/hello.sing", 'print("Hello, World!");\n'),
    "A+": ("aplus/hello.a", "'Hello, World!'\n"),
    # --- Enterprise / legacy ---
    "Natural": ("natural/hello.nsp", "WRITE 'Hello, World!'\nEND\n"),
    "Harbour": ("harbour/hello.prg", '? "Hello, World!"\n'),
    "GNU Smalltalk": ("gnu-smalltalk/hello.st", "'Hello, World!' displayNl.\n"),
    "Dylan": ("dylan/hello.dylan", 'format-out("Hello, World!\\n");\n'),
    "BeanShell": ("beanshell/hello.bsh", 'print("Hello, World!");\n'),
    "Ioke": ("ioke/hello.ik", '"Hello, World!" println\n'),
    "X10": ("x10/Hello.x10",
        'public class Hello {\n  public static def main(args: Rail[String]) {\n    Console.OUT.println("Hello, World!");\n  }\n}\n'),
    # --- Retro BASIC family ---
    "GW-BASIC": ("gwbasic/hello.bas", '10 PRINT "Hello, World!"\n'),
    "BBC BASIC": ("bbcbasic/hello.bbc", 'PRINT "Hello, World!"\n'),
    "PureBasic": ("purebasic/hello.pb",
        'OpenConsole()\nPrintN("Hello, World!")\n'),
    "Gambas": ("gambas/hello.module",
        'Public Sub Main()\n  Print "Hello, World!"\nEnd\n'),
    # --- Modern web-ish ---
    "Mint": ("mint/hello.mint",
        'component Main {\n  fun render : String {\n    "Hello, World!"\n  }\n}\n'),
    "Imba": ("imba/hello.imba", 'console.log "Hello, World!"\n'),
    "Civet": ("civet/hello.civet", 'console.log "Hello, World!"\n'),
}

EXTRA4_MARKUP: dict[str, tuple[str, str]] = {
    # --- Component / template engines ---
    "Svelte": ("svelte/Hello.svelte", '<p>Hello, World!</p>\n'),
    "Vue": ("vue/Hello.vue",
        '<template>\n  <p>Hello, World!</p>\n</template>\n'),
    "JSX": ("jsx/hello.jsx", 'const App = () => <p>Hello, World!</p>;\n'),
    "Astro": ("astro/hello.astro", '<p>Hello, World!</p>\n'),
    "Marko": ("marko/hello.marko", '<p>Hello, World!</p>\n'),
    "Razor": ("razor/hello.cshtml", '<p>@("Hello, World!")</p>\n'),
    "Blade": ("blade/hello.blade.php", '{{ "Hello, World!" }}\n'),
    "JSP": ("jsp/hello.jsp", '<%= "Hello, World!" %>\n'),
    "ASP (classic)": ("asp/hello.asp", '<%= "Hello, World!" %>\n'),
    "Velocity": ("velocity/hello.vm", '#set($g = "Hello, World!")$g\n'),
    "FreeMarker": ("freemarker/hello.ftl", '${"Hello, World!"}\n'),
    "Smarty": ("smarty/hello.tpl", '{"Hello, World!"}\n'),
    "Nunjucks": ("nunjucks/hello.njk", '{{ "Hello, World!" }}\n'),
    # --- Data / schema ---
    "JSON5": ("json5/hello.json5", '{ greeting: "Hello, World!" }\n'),
    "JSONC": ("jsonc/hello.jsonc",
        '{\n  // greeting\n  "greeting": "Hello, World!"\n}\n'),
    "NestedText": ("nestedtext/hello.nt", 'greeting: Hello, World!\n'),
    "SDLang": ("sdlang/hello.sdl", 'greeting "Hello, World!"\n'),
    "ASN.1": ("asn1/hello.asn1",
        'Greeting ::= SEQUENCE {\n  text UTF8String\n}\n'),
    "RAML": ("raml/hello.raml", '#%RAML 1.0\ntitle: Hello, World!\n'),
    "OpenAPI": ("openapi/hello.yaml",
        'openapi: 3.0.0\ninfo:\n  title: "Hello, World!"\n  version: "1.0"\npaths: {}\n'),
    "JSON Schema": ("jsonschema/hello.json",
        '{\n  "title": "Hello, World!",\n  "type": "string"\n}\n'),
    "XSD": ("xsd/hello.xsd",
        '<?xml version="1.0"?>\n<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n  <xs:element name="greeting" type="xs:string"/>\n</xs:schema>\n'),
}

PROGRAMS.update(EXTRA4_PROGRAMS)
MARKUP.update(EXTRA4_MARKUP)

# Alphuck: a 1:1 letter substitution of Brainfuck — derive it for correctness.
_BF_TO_ALPHUCK = {
    ">": "a", "<": "c", "+": "e", "-": "i", ".": "j", ",": "o", "[": "p", "]": "s",
}
PROGRAMS["Alphuck"] = (
    "alphuck/hello.alph",
    "".join(_BF_TO_ALPHUCK[c] for c in _bf_source if c in _BF_TO_ALPHUCK) + "\n",
)


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
