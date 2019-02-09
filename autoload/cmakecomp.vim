if !has('python3') || version < 700
  finish
endif

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

python3 << PYCMAKEEOF
import sys
import vim

sys.path.append(vim.eval("s:plugin_path"))
import cmakecomp

PYCMAKEEOF

function! cmakecomp#Complete(findstart, base)
    if a:findstart
        let line = getline('.')
        let idx = col('.') - 1
        let hasleftbrace = 0
        while idx > 0
            let idx -= 1
            let c = line[idx]
            if c =~ '\v[a-zA-Z0-9_]'
                continue
            else
                return idx+1
            endif
        endwhile
        return 0
    else
        execute 'python3 cmakecomp.complete("' . a:base . '")'
        call sort(g:cmakecomp_dict)
        return g:cmakecomp_dict
    endif
endfunction

