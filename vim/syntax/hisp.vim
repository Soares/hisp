" Hisp syntax file
" Language:    Hisp
" Maintainer:  Nathanel Soares <nate@natesoares.com>
" Last Change: Dec 11, 2010
" Version:     1
" URL:	       http://hisp.natesoares.com

" ---------------------------------------------------------------------
"  Load Once: {{{1
" For vim-version 5.x: Clear all syntax items
" For vim-version 6.x: Quit when a syntax file was already loaded

set ignorecase
syn case ignore

syn keyword hispTodo contained TODO FIXME XXX NOTE


syn region hispNativeComment start="{!" end="}" contains=hispTodo containedin=hispDjangoComment,hispHtmlComment,hispVariable,hispStrVariable,hispDoctype,hispString,hispLiteral,hispElem,hispCloser,hispBlock,hispMacro,hispBlockExtend,hispMacroExtend,hispAttribute,hispWord,hispClass,hispId
syn region hispDjangoComment start="{#" end="}" contains=hispTodo
syn region hispHtmlComment start="(!" end=")" contains=hispTodo
syn cluster hispComment contains=hispDjangoComment,hispHtmlComment

syn region hispVariable matchgroup=hispVarBrackets start="{[!#%]\@!" end="}" skip="\\\\\|\\}" contains=hispTodo,hispEscapeVar
syn region hispStrVariable matchgroup=hispVarBrackets start="{[!#%]\@!" end="}" skip="\\\\\|\\}" contains=hispTodo,hispEscapeVar,hispEscapeStr
syn region hispDoctype start="(\~" end=")"
syn region hispString start=+"+ end=+"+ skip="\\\\\|\\\"" contains=hispStrVariable,hispEscapeStr,@Spell
syn region hispLiteral start=+'+ end=+'+ skip="\\\\\|\\\'" contains=hispEscapeLit,@Spell

syn region hispElem matchgroup=hispElemColor start="(\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispAttribute,hispBlock,hispElem,hispMacro,hispLiteral,hispString,hispVariable,hispWord,hispClass,hispId,hispHtmlComment,hispDjangoComment,hispCloser
syn region hispCloser matchgroup=hispElemColor start="(\/\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispAttribute,hispClass,hispId,hispDjangoComment
syn region hispBlock start="{%" end="}" contains=hispBlockExtend,hispString,hispLiteral,hispHtmlComment,hispDjangoComment
syn region hispMacro matchgroup=hispMacroColor start="(%\s*\(\w\|-\)\+" end=")" contains=hispMacroExtend,hispAttribute,hispElem,hispCloser,hispBlock,hispVariable,hispHtmlComment,hispDjangoComment

syn region hispBlockExtend matchgroup=hispExtend start="\~" end="}\@=" contained contains=hispLiteral,hispString,hispBlock,hispElem,hispCloser,hispMacro,hispVariable,hispDoctype,hispComment
syn region hispMacroExtend matchgroup=hispExtend start="\~" end=")\@=" contained contains=hispLiteral,hispString,hispBlock,hispElem,hispCloser,hispMacro,hispAttribute,hispVariable,hispComment
syn region hispAttribute matchgroup=hispAttrParens start="(:\(\w\|-\)\+" end=")" contained contains=hispDjangoComment

syn match hispWord "\s\@<=[^{("~ \t\n)}]\+" contained
syn match hispClass "\s\@<!\.\(\w\|-\)\+" contained containedin=hispElemColor
syn match hispId "\s\@<!#\(\w\|-\)\+" contained containedin=hispElemColor
syn match hispEscapeStr +\(\\"\|\\\\\)+ contained
syn match hispEscapeLit +\(\\'\|\\\\\)+ contained
syn match hispEscapeVar +\(\\}\|\\\\\)+ contained

hi def link hispWord Normal
hi def link hispClass PreProc
hi def link hispId Identifier

hi def link hispElemColor Statement
hi def link hispMacroColor Identifier
hi def link hispBlock PreProc

hi def link hispVarBrackets PreProc
hi def link hispVariable Constant
hi def link hispStrVariable Constant

hi def link hispAttrParens Type
hi def link hispAttribute Constant

hi def link hispExtend Special
hi def link hispEscapeStr Special
hi def link hispEscapeVar Special
hi def link hispEscapeLit Special

hi def link hispString String
hi def link hispLiteral String

hi def link hispDoctype Include
hi def link hispHtmlComment PreProc
hi def link hispDjangoComment Comment
hi def link hispNativeComment Comment
hi def link hispTodo Todo
