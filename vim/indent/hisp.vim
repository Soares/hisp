" Description:	hisp indenter
" Author:	    Nate Soares
" Last Change:	Dec 12 2010

" Only load this indent file when no other was loaded.
if exists("b:did_indent")
    finish
endif
let b:did_indent = 1

setlocal autoindent nosmartindent
setlocal sts=2 sw=2 tabstop=2 et
setlocal indentexpr=GetHispIndent(v:lnum)
setlocal indentkeys=o,O

" Only define the function once.
if exists("*GetHispIndent")
  finish
endif

function! s:delta(lnum)
    let line = getline(a:lnum)
    let len = strlen(line)
    let delta=0
    let i=0
    while i <= len
        if synIDattr(synID(a:lnum, i, 0), 'name') !~? 'hisp\(HtmlComment\|String\|NativeComment\|DjangoComment\|Literal\)'
            if line[i] == "(" || line[i] == "{"
                " echo '(' . synIDattr(synID(a:lnum, i, 0), 'name')
                let delta = delta + 1
            elseif line[i] == ")" || line[i] == "}"
                " echo ')' . synIDattr(synID(a:lnum, i, 0), 'name')
                let delta = delta - 1
            endif
        endif
        let i = i + 1
    endwhile
    return delta
endfunction

function! GitHispIndent(lnum)
    if a:lnum == 0 | return 0 | endif
    let indent = indent(prev)
    let delta = s:delta(prevnonblack(a:lnum))
    return indent + delta * &sw
endfunction
