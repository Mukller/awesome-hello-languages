package Hello;
  (* synthesize *)
  module mkHello(Empty);
    rule r;
      $display("Hello, World!");
      $finish;
    endrule
  endmodule
endpackage
