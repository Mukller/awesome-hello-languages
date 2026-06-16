@.str = private constant [15 x i8] c"Hello, World!\0A\00"

declare i32 @puts(i8*)

define i32 @main() {
  %s = getelementptr [15 x i8], [15 x i8]* @.str, i64 0, i64 0
  call i32 @puts(i8* %s)
  ret i32 0
}
