module hello::greeting {
    use std::debug;
    public fun say() {
        debug::print(&b"Hello, World!");
    }
}
