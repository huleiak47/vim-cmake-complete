if exists('vim_cmake_complete_loaded') || &cp || !has('python3') || version < 700
    finish
endif
let vim_cmake_complete_loaded = 1

autocmd FileType cmake set omnifunc=cmakecomp#Complete

