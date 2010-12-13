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

runtime! syntax/html.vim
syn keyword hispTodo contained TODO FIXME XXX NOTE
syn include @htmlJavaScript syntax/javascript.vim

syn region hispNativeComment start="{!" end="}" contains=hispTodo containedin=hispDjangoComment,hispHtmlComment,hispVariable,hispStrVariable,hispDoctype,hispString,hispLiteral,hispElem,hispCloser,hispBlock,hispMacro,hispBlockExtend,hispMacroExtend,hispAttribute,hispWord,hispClass,hispId
syn region hispDjangoComment start="{#" end="}" contains=hispTodo
syn region hispHtmlComment start="(!" end=")" contains=hispTodo
syn cluster hispComment contains=hispDjangoComment,hispHtmlComment

syn region hispVariable matchgroup=hispVarBrackets start="{[!#%]\@!" end="}" skip="\\\\\|\\}" contains=hispTodo,hispEscapeVar
syn region hispStrVariable matchgroup=hispVarBrackets start="{[!#%]\@!" end="}" skip="\\\\\|\\}" contains=hispTodo,hispEscapeVar,hispEscapeStr
syn region hispDoctype start="(\~" end=")"
syn region hispString start=+"+ end=+"+ skip="\\\\\|\\\"" contains=hispStrVariable,hispEscapeStr,@Spell
syn region hispLiteral start=+'+ end=+'+ skip="\\\\\|\\\'" contains=hispEscapeLit,@Spell
syn region hispCdata keepend start="<" end=">" skip="\\\\\|\\>" contains=hispEscapeBrak
syn region hispJavaScript keepend matchgroup=hispBrackets start="<{!\(js\|javascript\)}" end=">" skip="\\\\\|\\>" contains=hispEscapeBrak,@htmlJavascript
syn region hispCss keepend matchgroup=hispBrackets start="<{!css}" end=">" contains=hispEscapeBrak,@htmlCss

syn region hispElem matchgroup=hispElemColor start="(\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispCdata,hispAttribute,hispBlock,hispElem,hispMacro,hispLiteral,hispString,hispVariable,hispWord,hispClass,hispId,hispHtmlComment,hispDjangoComment,hispCloser,hispJavaScript,hispCss
syn region hispCloser matchgroup=hispElemColor start="(\/\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispAttribute,hispClass,hispId,hispDjangoComment
syn region hispBlock start="{%" end="}" skip="\\\\\|\\}\|\\\~" contains=hispEscapeVar,hispEscapeExt,hispBlockExtend,hispString,hispCdata
syn region hispMacro matchgroup=hispMacroColor start="(%\s*\(\w\|-\)\+" end=")" contains=hispMacroExtend,hispAttribute,hispElem,hispCloser,hispBlock,hispVariable,hispHtmlComment,hispDjangoComment,hispCdata

syn region hispBlockExtend matchgroup=hispExtend start="\~" end="}\@=" contained contains=hispLiteral,hispString,hispBlock,hispElem,hispCloser,hispMacro,hispVariable,hispDoctype,hispComment,hispCdata
syn region hispMacroExtend matchgroup=hispExtend start="\~" end=")\@=" contained contains=hispLiteral,hispString,hispBlock,hispElem,hispCloser,hispMacro,hispAttribute,hispVariable,hispComment,hispCdata
syn region hispAttribute matchgroup=hispAttrParens start="(:\(\w\|-\)\+" end=")" contained contains=hispDjangoComment

syn match hispWord "\s\@<=[^{(<"~ \t\n>)}]\+" contained
syn match hispClass "\s\@<!\.\(\w\|-\)\+" contained containedin=hispElemColor
syn match hispId "\s\@<!#\(\w\|-\)\+" contained containedin=hispElemColor
syn match hispEscapeStr +\(\\"\|\\\\\)+ contained
syn match hispEscapeLit +\(\\'\|\\\\\)+ contained
syn match hispEscapeVar +\(\\}\|\\\\\)+ contained
syn match hispEscapeExt +\(\\\~\|\\\\\)+ contained
syn match hispEscapeBrak +\(\\>\|\\\\\)+ contained

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

hi def link hispExtend Statement
hi def link hispEscapeStr Special
hi def link hispEscapeVar Special
hi def link hispEscapeLit Special
hi def link hispEscapeExt Special
hi def link hispEscapeBrak Special

hi def link hispString String
hi def link hispLiteral String
hi def link hispCdata String
hi def link hispBrackets String

hi def link hispDoctype Include
hi def link hispHtmlComment PreProc
hi def link hispDjangoComment Comment
hi def link hispNativeComment Comment
hi def link hispTodo Todo
