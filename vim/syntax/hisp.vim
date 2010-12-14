" Hisp syntax file
" Language:    Hisp
" Maintainer:  Nathanel Soares <nate@natesoares.com>
" Last Change: Dec 11, 2010
" Version:     1
" URL:	       http://hisp.natesoares.com

" ---------------------------------------------------------------------

set ignorecase
syn case ignore

runtime! syntax/html.vim
syn include @htmlJavaScript syntax/javascript.vim

syn keyword hispTodo contained TODO FIXME XXX NOTE

syn region hispNativeComment start="{!" end="!}" skip="\\\\\|\\!" keepend contains=hispTodo containedin=@hispAll
syn region hispDjangoComment start="{#" end="#}" skip="\\\\\|\\#" contains=hispTodo
syn region hispHtmlComment start="(!" end="!)" skip="\\\\\|\\!" contains=hispTodo
syn cluster hispLiveComment contains=hispDjangoComment,hispHtmlComment
syn cluster hispAll contains=@hispLiveComment

syn region hispDoctype start="(\~" end=")"
syn region hispElement matchgroup=hispDelimTag start="(\s*\(#\@=\|\.\@=\|\w\|[-:]\)\+" end=")" contains=hispAttribute,@hispConstant,@hispStatement
syn region hispSelfCloser matchgroup=hispDelimTag start="(\s*\(#\@=\|\.\@=\|\w\|[-:]\)\+\/" end=")" contains=hispAttribute,hispDjangoComment
syn cluster hispTag contains=hispElement,hispSelfCloser

syn region hispMacro matchgroup=hispDelimMacro start="(%\s*\(#\@=\|\.\@=\|\w\|-\)\+" end=")" contains=hispMacroExtend,hispAttribute,hispElem,hispCloser,hispBlock,hispVariable,hispHtmlComment,hispDjangoComment,hispCdata
syn region hispJavaScript keepend matchgroup=hispNewlang start="(%javascript.*<" end=">\s*)" skip="\\\\\|\\>" contains=@htmlJavascript
syn region hispCSS keepend matchgroup=hispNewlang start="(%css.*<" end=">\s*)" skip="\\\\\|\\>" contains=@htmlCss
syn cluster hispMacros contains=hispMacro,hispJavaScript,hispCSS

syn region hispBlock start="{%" end="}" skip="\\\\\|\\}\|\\\~" contains=hispBlockExtend,hispString
syn cluster hispStatement contains=hispDoctype,@hispLiveComment,@hispTag,@hispMacros,hispBlock
syn cluster hispAll add=@hispStatement

syn region hispBlockExtend matchgroup=hispDelimExtend start="\~" end="}\@=" contained contains=@hispConstant,@hispStatement
syn region hispBlockString matchgroup=hispDelimExtend start="\~" end="}\@=" contained contains=@hispConstant,@hispStatement
syn region hispString start=+"+ end=+"+ skip="\\\\\|\\\"" contains=hispVariable,@Spell
syn region hispAttribute matchgroup=hispDelimAttr start="(:\(\w\|-\)\+" end=")" contained contains=@hispConstant,hispDjangoComment

syn region hispMacroArg matchgroup=hispDelimArg start="\s\@<!\[" end="\]" skip="\\\\\|\\\]" contained containedin=hispMacro
syn match hispClassAttr "\s\@<!\.\(\w\|-\)\+" contained containedin=@hispTag,@hispMacros
syn match hispIdAttr "\s\@<!#\(\w\|-\)\+" contained containedin=@hispTag,@hispMacros
syn cluster hispTagAttr contains=hispClassAttr,hispIdAttr
syn cluster hispAll add=@hispTagAttr

syn region hispString start=+"+ end=+"+ skip="\\\\\|\\\"" contains=hispVariable,@Spell
syn region hispLiteral start=+'+ end=+'+ skip="\\\\\|\\\'" contains=@Spell
syn region hispCDATA start="<" end=">" skip="\\\\\|\\>"
syn cluster hispText contains=hispString,hispLiteral,hispCDATA

syn region hispVariable matchgroup=hispDelimVar start="{[!#%]\@!" end="}" skip="\\\\\|\\}"
syn cluster hispDjango contains=hispDjangoComment,hispBlock,hispVariable
syn cluster hispConstant contains=@hispText,hispVariable
syn cluster hispAll add=@hispConstant

syn match hispWord "\s\@<=[^"' \t\n<>(){}]\+" contained containedin=hispMacro,@hispTag
syn cluster hispAll add=hispWord

syn match hispEscapeBang +\(\\!\|\\\\\)+ contained containedin=hispNativeComment,hispHtmlComment
syn match hispEscapeHash +\(\\#\|\\\\\)+ contained containedin=hispDjangoComment
syn match hispEscapeStr +\(\\"\|\\\\\)+ contained containedin=hispString,hispBlockString
syn match hispEscapeLit +\(\\'\|\\\\\)+ contained containedin=hispLiteral
syn match hispEscapeBrak +\(\\}\|\\\\\)+ contained containedin=hispVariable
syn match hispEscapeParen +\(\\)\|\\\\\)+ contained containedin=hispVariable
syn match hispEscapeBlock +\(\\}\|\\\~\|\\\\\)+ contained containedin=hispBlock
syn match hispEscapeCDATA +\(\\>\|\\\\\)+ contained containedin=hispCDATA,hispJavaScript,hispCSS
syn cluster hispEscape contains=hispEscapeStr,hispEscapeLit,hispEscapeVar,hispEscapeBlock,hispEscapeCDATA

hi def link hispTodo Todo

hi def link hispClassAttr PreProc
hi def link hispIdAttr Identifier

hi def link hispHtmlComment PreProc
hi def link hispNativeComment Comment
hi def link hispDjangoComment Comment

hi def link hispDoctype PreProc
hi def link hispDelimTag Statement
hi def link hispDelimMacro Identifier
hi def link hispBlock PreProc

hi def link hispDelimAttr Type

hi def link hispDelimVar PreProc
hi def link hispDelimArg PreProc
hi def link hispMacroArg String
hi def link hispString String
hi def link hispLiteral String
hi def link hispCDATA String

hi def link hispAttrParens Type
hi def link hispAttribute Constant

hi def link hispDelimExtend Statement
hi def link hispEscapeStr Special
hi def link hispEscapeVar Special
hi def link hispEscapeLit Special
hi def link hispEscapeBlock Special
hi def link hispEscapeCDATA Special
hi def link hispEscape Special
